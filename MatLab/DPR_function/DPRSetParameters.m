function options = DPRSetParameters(PSF,varargin)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
% INPUT:
% PSF = FWHM in pixel numbers of the imaging system
% 
% gain: scaling of pixel shift along gradient 
%   1 - by default
%   2 - higher resolution enhancement
% 
% window_radius: the radius (in pixels) of window to search for the local 
%                minimum, at least the size of the largest structures in 
%                the image 
%   If not input: set as 10 * PSF 
%   
% temporal:
%   'mean' - temporal average
%   'var' - temporal variance
%   If not choose: Output an image stack 
%
% 
% OUTPUT:
% 
% options: parameters for PSF, window radius, and temporal process used in 
%          DPR  
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Read inputs from varagin
Names = [
    'gain            '
    'background      '
    'temporal        '
    ];
[m,~] = size(Names);
names = lower(Names);
options = [];

% Combine all leading options structures o1, o2, ... in l1Set(o1,o2,...).
options = [];
for j = 1:m
    eval(['options.' Names(j,:) '= [];']);
end

% Check whether there is varagin
if isempty(varargin)
    options.gain = 1;
    options.background = ceil(10 * PSF);
    options.temporal = [];
end

i = 1;
while i <= nargin - 1
    arg = varargin{i};
    if ischar(arg), break; end
    if ~isempty(arg)                      % [] is a valid options argument
        if ~isa(arg,'struct')
            error(sprintf('Wrong argument'));
        end
        for j = 1:m
            if any(strcmp(fieldnames(arg),deblank(Names(j,:))))
                eval(['val = arg.' Names(j,:) ';']);
            else
                val = [];
            end
            if ~isempty(val)
                eval(['options.' Names(j,:) '= val;']);
            end
        end
    end
    i = i + 1;
end

% A finite state machine to parse name-value pairs.
if rem(nargin-1-i+1,2) ~= 0
    error('Arguments must occur in name-value pairs.');
end

% name-value pairing
expectval = 0; % start expecting a name, not a value
i = 1;
while i <= nargin-1
    arg = varargin{i};   
    if ~expectval
        if ~ischar(arg)
            error(sprintf('Invalid input'));
        end
        
        lowArg = lower(arg);
        j = strmatch(lowArg,names);
        if isempty(j)                       % if no matches
            error(sprintf('Invalid input'));
        end
        expectval = 1;                      % we expect a value next        
    else
        eval(['options.' Names(j,:) '= arg;']);
        expectval = 0;     
    end
    i = i + 1;
end

% If no input for certain argument
Values = [
    {1}
    {ceil(10*PSF)}
    {''}
    ];

for j = 1:m
    if eval(['isempty(options.' Names(j,:) ')'])
        eval(['options.' Names(j,:) '= Values{j};']);
    end
end

end