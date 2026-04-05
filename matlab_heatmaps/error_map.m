%rk4_plte_landscape.m
%generates a high-res
%truncation error (pl

clear; clc; close all;

%% 1. parameter space
N = 1000; %slightly higher reso
c2_vec = linspace(0.005, 0.995, N);
c3_vec = linspace(0.005, 0.995, N);
[C2, C3] = meshgrid(c2_vec, c3_vec);
PLTE_grid = zeros(N, N);

%% 2. anonymous funct
calc_PLTE = @(A, w, c) sqrt( ...
    ( w(:)' * c(:).^4 - 1/5 )^2 + ...                             %e1
    ( (w(:) .* c(:).^2)' * A * c(:) - 1/10 )^2 + ...              %e2
    ( (w(:) .* c(:))' * A * c(:).^2 - 1/15 )^2 + ...              %e3
    ( w(:)' * A * c(:).^3 - 1/20 )^2 + ...                        %e4
    ( (w(:) .* c(:))' * A * A * c(:) - 1/30 )^2 + ...             %e5
    ( w(:)' * ( (A*c(:)) .* (A*c(:)) ) - 1/20 )^2 + ...           %e6
    ( w(:)' * A * (c(:) .* (A*c(:))) - 1/40 )^2 + ...             %e7
    ( w(:)' * A * A * c(:).^2 - 1/60 )^2 + ...                    %e8
    ( -1/120 )^2 ...                                              %e9
);

%% 3. evaluate the gr
for i = 1:N
    for j = 1:N
        c2 = C2(i,j);
        c3 = C3(i,j);
        
        %handle the c2 = c3 s
        if abs(c2 - c3) < 1e-4
            %in the limit c2 -> c
            %this corresponds to 
            %we use the standard 
            w2 = 1/3; w3 = 1/3; w4 = 1/6; w1 = 1/6;
            a21 = c2; a32 = 1/2; a31 = c2 - a32;
            a43 = 1; a42 = 0; a41 = 0;
        else
            %standard solver for 
            if abs(c2 - 1) < 1e-3 || abs(c3 - 1) < 1e-3
                PLTE_grid(i,j) = NaN;
                continue;
            end
            
            M = [c2, c3, 1; c2^2, c3^2, 1; c2^3, c3^3, 1];
            rhs = [1/2; 1/3; 1/4];
            w234 = M \ rhs;
            w2 = w234(1); w3 = w234(2); w4 = w234(3);
            w1 = 1 - sum(w234);
            
            %spatial weights
            if abs(w3) < 1e-7 || abs(w4) < 1e-7
                PLTE_grid(i,j) = NaN; continue;
            end
            
            a32 = 1 / (24 * w3 * c2 * (1 - c3));
            a43 = 1 / (24 * w4 * a32 * c2);
            a42 = (1/6 - w3 * c2 * a32 - w4 * c3 * a43) / (w4 * c2);
            a21 = c2; a31 = c3 - a32; a41 = 1 - a42 - a43;
        end
        
        %build and calculate
        w = [w1; w2; w3; w4];
        c = [0; c2; c3; 1];
        A = [0, 0, 0, 0; a21, 0, 0, 0; a31, a32, 0, 0; a41, a42, a43, 0];
        PLTE_grid(i,j) = calc_PLTE(A, w, c);
    end
end

%% 4. optimized visua
%1. prevent log10(0) 
%this prevents 'holes
log_PLTE = log10(max(PLTE_grid, eps));

%2. create figure wit
%using a square ratio
fig = figure('Name', 'RK4 PLTE Landscape', 'Color', 'w', 'Position', [100, 100, 800, 800]);

%3. generate the cont
%increased levels to 
contourf(C2, C3, log_PLTE, 200, 'LineColor', 'none');
colormap(turbo);

%4. strip the ui (the
axis off;           %remove ticks and num
axis tight;         %ensure data fills th
hold on;

%5. force zero margin
%this is the crucial 
%we set all margins t
ax = gca;
set(ax, 'Position', [0 0 1 1], 'Units', 'Normalized');
set(ax, 'LooseInset', get(ax, 'TightInset')); 

%6. final polish
xlim([0 1]); 
ylim([0 1]); 
hold off;

%7. high-res export
%'backgroundcolor', '
exportgraphics(fig, 'rk4_heatmap.png', 'Resolution', 600, 'BackgroundColor', 'none');

fprintf('Export Complete: rk4_heatmap.png is ready for Manim.\n');