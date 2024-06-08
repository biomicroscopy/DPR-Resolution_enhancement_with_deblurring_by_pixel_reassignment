%% Start the parallel computing
clear,clc
gcp

%% Add path and direction of the images

addpath(genpath('DPR_function'))
data_folder = 'LS'; % folder  where all the files are located.
filetype = 'tif'; % type of files to be processed

%% Set image parameter

file_name = 'test_image';
n = 60; % frame number

%% Prepare image for saving
save_folder = 'DPR_image'; % folder where all the DPR-enhanced images are saved.
mkdir save_folder

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
    %run on Macbook
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
