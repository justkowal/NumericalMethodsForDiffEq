%rk4_interactive_land
%generates a 2d plte 
%hover over any point

clear; clc; close all;

%% 1. parameter space
N = 1000; 
c2_vec = linspace(0.005, 0.995, N);
c3_vec = linspace(0.005, 0.995, N);
[C2, C3] = meshgrid(c2_vec, c3_vec);
PLTE_grid = zeros(N, N);

%% 2. error calculati
%defining this as a s
calc_PLTE = @(A, w, c) sqrt( ...
    ( w(:)' * c(:).^4 - 1/5 )^2 + ...
    ( (w(:) .* c(:).^2)' * A * c(:) - 1/10 )^2 + ...
    ( (w(:) .* c(:))' * A * c(:).^2 - 1/15 )^2 + ...
    ( w(:)' * A * c(:).^3 - 1/20 )^2 + ...
    ( (w(:) .* c(:))' * A * A * c(:) - 1/30 )^2 + ...
    ( w(:)' * ( (A*c(:)) .* (A*c(:)) ) - 1/20 )^2 + ...
    ( w(:)' * A * (c(:) .* (A*c(:))) - 1/40 )^2 + ...
    ( w(:)' * A * A * c(:).^2 - 1/60 )^2 + ...
    ( -1/120 )^2 ...
);

%% 3. pre-calculate t
%we perform the calcu
for i = 1:N
    for j = 1:N
        c2 = C2(i,j);
        c3 = C3(i,j);
        
        %solve for weights an
        [A, w, c, valid] = solve_rk4_params(c2, c3);
        
        if ~valid
            PLTE_grid(i,j) = NaN;
        else
            PLTE_grid(i,j) = calc_PLTE(A, w, c);
        end
    end
end

%% 4. visualization
log_PLTE = log10(PLTE_grid);
fig = figure('Name', 'Interactive RK4 Explorer', 'Color', 'w', 'Position', [100, 100, 1000, 800]);

%create the heatmap
h = imagesc(c2_vec, c3_vec, log_PLTE);
set(gca, 'YDir', 'normal'); %correct axis orienta
colormap(turbo);
cb = colorbar;
cb.Label.String = 'log10(Principal Local Truncation Error)';
cb.Label.FontWeight = 'bold';

hold on;
title('Interactive RK4 PLTE Landscape', 'FontSize', 14);
xlabel('c_2', 'FontSize', 12); ylabel('c_3', 'FontSize', 12);
grid on;

%add the data tip cus
dtt = datacursormode(fig);
set(dtt, 'UpdateFcn', @(obj, event_obj) customDataTip(obj, event_obj));
set(dtt, 'SnapToDataVertex', 'off'); %allow smooth hoverin
set(dtt, 'Enable', 'on');

%% 5. helper function
function [A, w, c, valid] = solve_rk4_params(c2, c3)
    valid = true;
    A = zeros(4,4); w = zeros(4,1); c = [0; c2; c3; 1];
    
    %singularity handling
    if abs(c2 - c3) < 1e-4
        if abs(c2 - 0.5) < 0.1
            %near the classic rk4
            w = [1/6; 1/3; 1/3; 1/6];
            A = [0 0 0 0; c2 0 0 0; 0 c3 0 0; 0 0 1 0];
        else
            valid = false; return;
        end
    else
        %standard solver logi
        if abs(c2 - 1) < 1e-3 || abs(c3 - 1) < 1e-3
            valid = false; return;
        end
        
        M = [c2, c3, 1; c2^2, c3^2, 1; c2^3, c3^3, 1];
        rhs = [1/2; 1/3; 1/4];
        w234 = M \ rhs;
        w = [1 - sum(w234); w234];
        
        %internal coefficient
        if abs(w(3)) < 1e-7 || abs(w(4)) < 1e-7
            valid = false; return;
        end
        
        a32 = 1 / (24 * w(3) * c2 * (1 - c3));
        a43 = 1 / (24 * w(4) * a32 * c2);
        a42 = (1/6 - w(3) * c2 * a32 - w(4) * c3 * a43) / (w(4) * c2);
        
        A = [0, 0, 0, 0; 
             c2, 0, 0, 0; 
             c3-a32, a32, 0, 0; 
             1-a42-a43, a42, a43, 0];
    end
end

%% 6. data tip callba
function txt = customDataTip(~, event_obj)
    pos = event_obj.Position;
    c2 = pos(1);
    c3 = pos(2);
    
    [A, w, c, valid] = solve_rk4_params(c2, c3);
    
    if ~valid
        txt = 'Invalid Region (Singularity)';
    else
        %calculate error at t
        %note: calc_plte is r
        E1 = ( w(:)' * c(:).^4 - 1/5 );
        E2 = ( (w(:) .* c(:).^2)' * A * c(:) - 1/10 );
        %... (we simplify for
        
        txt = { ...
            sprintf('Coordinates: c2=%.3f, c3=%.3f', c2, c
            sprintf('log10(Error): %.4f', event_obj.targ
            '---------------------------', ...
            'Weights (w1, w2, w3, w4):', ...
            sprintf('[%.4f, %.4f, %.4f, %.4
            'Matrix A (Lower Triangular):', ...
            sprintf('a21: %.4f', a(2,1)), ...
            sprintf('a31, a32: [%.4f, %.4f]', a(3,1),
            sprintf('a41, a42, a43: [%.4f, %.4f, %.4f]', a
        };
    end
end