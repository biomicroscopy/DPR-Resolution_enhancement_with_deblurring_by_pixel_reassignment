%% Start the parallel computing


clear,clc
gcp

%% Add path and direction of the images


addpath(genpath('DPR_function'))
data_folder = 'Test_image'; % folder  where all the files are located.
filetype = 'tif'; % type of files to be processed


%% Load the image


file_name = 'test_image';
n = 60; % frame number
img = [];
% Input image requires the DOUBLE data type
parfor i = 1:n
%     % run on Windows
%     img(:,:,i) = double(imread([data_folder,'\',file_name,'.',filetype],i)); 
    %run on Macbook
    img(:,:,i) = double(imread([data_folder,'/',file_name,'.',filetype],i)); 
end

%% Set DPR parameters

% PSF FWHM in pixels, background is the radius of the local-minimum filter in pixels, temporal analysis
PSF = 4;
options = DPRSetParameters(PSF,'gain',2,'background',10,'temporal','mean'); 

%% Run DPR

% Input image requires the DOUBLE data type
% Output the DPR-enhanced image and the magnified raw images for comparison
[I_DPR,raw_magnified] = DPRStack(img,PSF,options);

% % For single-frame image
% [I_DPR,raw_magnified] = DPR_UpdateSignle_mex(img,PSF,options);

%% Svae image as needed
mkdir DPR_image
save_folder = 'DPR_image'; % folder where all the DPR-enhanced images are saved.

save_tiff_img(I_DPR,save_folder,'testimage_DPR2')
cd ..
save_tiff_img(mean(raw_magnified,3),save_folder,'testiamge_magnified')

