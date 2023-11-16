function [single_frame_I_out,single_frame_I_magnified,gain,window_radius] = DPR_UpdateSingle(I_in,PSF,options)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% INPUT:
% PSF = FWHM in pixel numbers of the imaging system
%       If not known, PSF can be simply assumed as (0.61 * lambda_emission[um] / NA) / pixel_size[um]      
%
% options: parameters for PSF, window radius, and temporal process used in 
%          DPR 
% 
%   gain: scaling of pixel shift along gradient 
%       1 - by default
%       2 - higher resolution enhancement
% 
%   background: the radius (in pixels) of the local minimum filter
%               typically the size of the largest structures in the image        
%               If not defined: set as 17 * PSF 
%   
%   temporal:
%       'mean' - temporal average
%       'var' - temporal variance
%       If not choose: Output an image stack 
%
% OUTPUT:
% I_out: Reconstructed image from DPR
% I_magnified: Magnified raw image/image stack (dependent on the input)
%
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Read inputs from options
gain = options(1).gain;
window_radius = ceil(options(1).background);

%% Set parameter for image upscaling
% Convert PSF to the 1/e radius
PSF = PSF/1.6651; 

% upscaled input image
[number_row_initial, number_column_initial] = size(I_in);
x0 = linspace(-0.5,0.5,number_column_initial)';
y0 = linspace(-0.5,0.5,number_row_initial)';
[X0,Y0] = meshgrid(x0,y0);
x = linspace(-0.5,0.5,round(5*number_column_initial/PSF))';  %upscaled image has 5 pixels per PSF (1/e radius) 
y = linspace(-0.5,0.5,round(5*number_row_initial/PSF))';
[X,Y] = meshgrid(x,y);

%% Set the Sobel kernel
sobelX = [1, 0, -1; 2, 0, -2; 1, 0, -1];
sobelY = [1, 2, 1; 0, 0, 0; -1, -2, -1];

%% DPR on single frames
single_frame_I_in = I_in - min(I_in(:));
local_minimum = zeros(number_row_initial,number_column_initial);
single_frame_I_in_localmin = zeros(number_row_initial,number_column_initial);
    for u = 1 : number_row_initial
        for v = 1 : number_column_initial
            % define sub window - window size: x times 1/e radius
            sub_window = single_frame_I_in(max(1,u-window_radius):min(number_row_initial,u+window_radius)...
                ,max(1,v-window_radius):min(number_column_initial,v+window_radius));
            % find local minimum in the local window
            local_minimum(u,v) = min(sub_window(:));
            % I - local_min(I)
            single_frame_I_in_localmin(u,v) = single_frame_I_in(u,v) - local_minimum(u,v);
        end
    end
% upscale
% I - local min - used to calculate gradient
single_frame_localmin_magnified=interp2(X0,Y0,single_frame_I_in_localmin,X,Y,'spline',0);   %upscaled (magnified) version of original image
single_frame_localmin_magnified(single_frame_localmin_magnified<0)=0;
single_frame_localmin_magnified=padarray(single_frame_localmin_magnified,[10 10],0,'both');    %prevents out of image displacements
% Raw image
single_frame_I_magnified = interp2(X0,Y0,single_frame_I_in,X,Y,'spline',0);
single_frame_I_magnified(single_frame_I_magnified<0)=0;
single_frame_I_magnified=padarray(single_frame_I_magnified,[10 10],0,'both');    
    
[number_row, number_column] = size(single_frame_I_magnified);
%%
%locally normalized version of Im
I_normalized=single_frame_localmin_magnified./(imgaussfilt(single_frame_localmin_magnified,10)+0.00001);
    
%calculate normalized gradients
gradient_y = imfilter(I_normalized, sobelX, 'conv', 'replicate');
gradient_x = imfilter(I_normalized, sobelY, 'conv', 'replicate');
    
%%
gradient_x=gradient_x./(I_normalized+0.00001);
gradient_y=gradient_y./(I_normalized+0.00001);
    
%%
%calculate pixel displacements
gain_value = 0.5 * gain + 1;
displacement_x=gain_value*gradient_x;
displacement_y=gain_value*gradient_y;
displacement_x(abs(displacement_x)>10)=0; %limit displacements to twice PSF size
displacement_y(abs(displacement_y)>10)=0;
    
%%
%calculate I_out with weighted pixel displacements
single_frame_I_out=zeros(number_row,number_column);
for nx=11:number_row-10
    for ny=11:number_column-10
        weighted1=(1-abs(displacement_x(nx,ny)-fix(displacement_x(nx,ny))))*(1-abs(displacement_y(nx,ny)-fix(displacement_y(nx,ny))));
        weighted2=(1-abs(displacement_x(nx,ny)-fix(displacement_x(nx,ny))))*(abs(displacement_y(nx,ny)-fix(displacement_y(nx,ny))));
        weighted3=(abs(displacement_x(nx,ny)-fix(displacement_x(nx,ny))))*(1-abs(displacement_y(nx,ny)-fix(displacement_y(nx,ny))));
        weighted4=(abs(displacement_x(nx,ny)-fix(displacement_x(nx,ny))))*(abs(displacement_y(nx,ny)-fix(displacement_y(nx,ny))));
        coordinate1=[fix(displacement_x(nx,ny)), fix(displacement_y(nx,ny))];
        coordinate2=[fix(displacement_x(nx,ny)), fix(displacement_y(nx,ny)+sign(displacement_y(nx,ny)))];
        coordinate3=[fix(displacement_x(nx,ny))+sign(displacement_x(nx,ny)), fix(displacement_y(nx,ny))];
        coordinate4=[fix(displacement_x(nx,ny))+sign(displacement_x(nx,ny)), fix(displacement_y(nx,ny))+sign(displacement_y(nx,ny))];
            
        % Shift I-local_min, use 'single_frame_localmin_magnified',
        % shift raw image, use 'single_frame_I_magnified'
        single_frame_I_out(nx+coordinate1(1),ny+coordinate1(2))=single_frame_I_out(nx+coordinate1(1),ny+coordinate1(2))+weighted1*single_frame_I_magnified(nx,ny);
        single_frame_I_out(nx+coordinate2(1),ny+coordinate2(2))=single_frame_I_out(nx+coordinate2(1),ny+coordinate2(2))+weighted2*single_frame_I_magnified(nx,ny);
        single_frame_I_out(nx+coordinate3(1),ny+coordinate3(2))=single_frame_I_out(nx+coordinate3(1),ny+coordinate3(2))+weighted3*single_frame_I_magnified(nx,ny);
        single_frame_I_out(nx+coordinate4(1),ny+coordinate4(2))=single_frame_I_out(nx+coordinate4(1),ny+coordinate4(2))+weighted4*single_frame_I_magnified(nx,ny);         
    end
end
  
%%
single_frame_I_out=single_frame_I_out(11:end-10,11:end-10);
single_frame_I_magnified=single_frame_I_magnified(11:end-10,11:end-10);
    
end
