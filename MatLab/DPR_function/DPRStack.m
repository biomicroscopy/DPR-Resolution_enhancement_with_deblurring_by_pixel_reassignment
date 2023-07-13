function [I_DPR,raw_magnified] = DPRStack(I_in,PSF,options)
%%
n = size(I_in,3);
I_DPR = []; raw_magnified = [];
%%
parfor i = 1 : n
    [single_I_DPR,single_raw_mag] = DPR_UpdateSignle_mex(I_in(:,:,i),PSF,options);
    I_DPR(:,:,i) = single_I_DPR;
    raw_magnified(:,:,i) = single_raw_mag;
end

%% Temporal process
temporal = string(options.temporal);
tp = [
    "mean"   
    "var"   ];
if ~isempty(temporal)
    k = strcmp(temporal,tp);
    if k(1,1) == 1
        I_DPR = mean(I_DPR,3);
    elseif k(2,1) == 1
        I_DPR = var(I_DPR,1,3);
    end
end

end