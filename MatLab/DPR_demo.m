%% Start the parallel computing
clear,clc
gcp

%% Add path and direction of the images
addpath(genpath('DPR_function'))
data_folder = 'Test_image'; % folder  where all the files are located.
filetype = 'tif'; % type of files to be processed

%% Set image parameter
file_name = 'sarcomere';

% Determine the number of frames in the image stack
image_info = imfinfo(fullfile(data_folder, [file_name, '.', filetype]));
n = numel(image_info); % Automatically determine the number of frames

%% Load the initial TIFF image
tiff_file_path = fullfile(data_folder, [file_name, '.', filetype]);
initial_image = imread(tiff_file_path, 'Index', 1); % Load the first frame

%% Prepare image for saving
save_folder = 'DPR_image'; % folder where all the DPR-enhanced images are saved.
if ~exist(save_folder, 'dir')
    mkdir(save_folder);
end

%% Set DPR parameters

% PSF FWHM in pixels, background is the radius of the local-minimum filter in pixels, temporal analysis
% If PSF is unknown, its FWHM in pixels can be simply estimated by (0.61*lambda/NA)/pixel_size. 
% lambda is the emission wavelength, NA is the numerical aperture of the objective
PSF = 4;
options = DPRSetParameters(PSF,'gain',2,'background',10,'temporal','mean'); 

%% Load the image
img = [];
% Input image requires the DOUBLE data type
parfor i = 1:n
%     % run on Windows
%     img(:,:,i) = double(imread([data_folder,'\',file_name,'.',filetype],i)); 
    % run on Macbook
    img(:,:,i) = double(imread([data_folder,'/',file_name,'.',filetype],i)); 
end

%% Run DPR

% Input image requires the DOUBLE data type
% Output the DPR-enhanced image and the magnified raw images for comparison
[I_DPR,raw_magnified] = DPRStack(img,PSF,options);

% % For single-frame image
% [I_DPR,raw_magnified] = DPR_UpdateSingle_mex(img,PSF,options);

save_tiff_img(I_DPR,save_folder,[file_name, '_DPR2'])
cd ..
save_tiff_img(mean(raw_magnified,3),save_folder,[file_name, '_magnified'])

%% Display the initial, magnified, result images for comparison
figure
subplot(1,3,1);
imagesc(initial_image)
colormap gray
title('Initial');

subplot(1,3,2)
imagesc(mean(raw_magnified,3))
colormap gray
title("DprMagnified")

subplot(1,3,3)
imagesc(I_DPR)
colormap gray
title("DprResult")

% Set a reasonable width for the figure window
set(gcf, 'Position', [100, 100, 1200, 400]); % Adjust as needed for better visualization

