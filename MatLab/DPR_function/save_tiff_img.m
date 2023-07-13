function save_tiff_img(img,save_folder,save_name)

% a image length
% b image width
cd(save_folder)
n = size(img);
[a b c] = size(img);
if length(n) == 3
    n = n(1,3);
    for j = 1:1:n % # of slices
        if j == 1
            t = Tiff([save_name,'.tif'],'w');
        else
            t = Tiff([save_name,'.tif'], 'a');
        end
        t.setTag('ImageLength', a);
        t.setTag('ImageWidth', b);
        t.setTag('Photometric', Tiff.Photometric.MinIsBlack);
        setTag(t,'SampleFormat',Tiff.SampleFormat.IEEEFP);%IEEEFP
        t.setTag('BitsPerSample', 64);
        t.setTag('SamplesPerPixel', 1);
        t.setTag('PlanarConfiguration', Tiff.PlanarConfiguration.Chunky);
        t.write(img(:,:,j));
        t.close;
    end
else
    t = Tiff([save_name,'.tif'],'w');
    t.setTag('ImageLength', a);
    t.setTag('ImageWidth', b);
    t.setTag('Photometric', Tiff.Photometric.MinIsBlack);
    setTag(t,'SampleFormat',Tiff.SampleFormat.IEEEFP);%IEEEFP
    t.setTag('BitsPerSample', 64);
    t.setTag('SamplesPerPixel', 1);
    t.setTag('PlanarConfiguration', Tiff.PlanarConfiguration.Chunky);
    t.write(img);
    t.close;
end
end