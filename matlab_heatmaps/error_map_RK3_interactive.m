%rk3_interactive_land
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
%instead of taking th
%we isolate e_1 to sh

%calc_plte = @(a, w, 
%( w(:)' * c(:).^3 - 
%);


%full function with w
calc_PLTE = @(A, w, c) sqrt( ...
    1 * ( w(:)' * c(:).^3 - 1/4 )^2 + ...
    1   * ( (w(:) .* c(:))' * A * c(:) - 1/8 )^2 + ...
    1   * ( w(:)' * A * c(:).^2 - 1/12 )^2 + ...
    1   * ( w(:)' * A * A * c(:) - 1/24 )^2 ...
);


%% 3. pre-calculate t
for i = 1:N
    for j = 1:N
        c2 = C2(i,j);
        c3 = C3(i,j);
        
        %solve for weights an
        [A, w, c, valid] = solve_rk3_params(c2, c3);
        
        if ~valid
            PLTE_grid(i,j) = NaN;
        else
            PLTE_grid(i,j) = calc_PLTE(A, w, c);
        end
    end
end

%% 4. visualization
log_PLTE = log10(PLTE_grid);
fig = figure('Name', 'Interactive RK3 Explorer', 'Color', 'w', 'Position', [100, 100, 1000, 800]);

%create the heatmap
h = imagesc(c2_vec, c3_vec, log_PLTE);
set(gca, 'YDir', 'normal'); %correct axis orienta
colormap(turbo);
cb = colorbar;
cb.Label.String = 'log10(Principal Local Truncation Error)';
cb.Label.FontWeight = 'bold';

hold on;
title('Interactive RK3 PLTE Landscape', 'FontSize', 14);
xlabel('c_2', 'FontSize', 12); ylabel('c_3', 'FontSize', 12);
grid on;

%--- add this to sect

%4.5 plot the optimal
%we split it into two
c2_left = linspace(0.005, 0.65, 500);
c3_left = (4*c2_left - 3) ./ (6*c2_left - 4);

c2_right = linspace(0.68, 0.995, 500);
c3_right = (4*c2_right - 3) ./ (6*c2_right - 4);

%plot as a thick whit
plot(c2_left, c3_left, 'w--', 'LineWidth', 2, 'DisplayName', 'Optimal O(h^4) Condition');
plot(c2_right, c3_right, 'w--', 'LineWidth', 2, 'HandleVisibility', 'off');

%force the viewing wi
axis([0 1 0 1]);
legend('Location', 'northeast', 'TextColor', 'w', 'Color', 'none');

%--------------------


%add the data tip cus
dtt = datacursormode(fig);
set(dtt, 'UpdateFcn', @(obj, event_obj) customDataTip(obj, event_obj));
set(dtt, 'SnapToDataVertex', 'off'); %allow smooth hoverin
set(dtt, 'Enable', 'on');

%% 5. helper function
function [A, w, c, valid] = solve_rk3_params(c2, c3)
    valid = true;
    A = zeros(3,3); w = zeros(3,1); c = [0; c2; c3];
    
    %singularity handling
    %c2=0 or c3=0 or c2=c
    %c2 = 2/3 causes w3 t
    if abs(c2 - c3) < 1e-4 || c2 < 1e-4 || c3 < 1e-4 || abs(c2 - 2/3) < 1e-4
        valid = false; return;
    end
    
    %solve for quadrature
    w(2) = (3*c3 - 2) / (6*c2*(c3 - c2));
    w(3) = (2 - 3*c2) / (6*c3*(c3 - c2));
    w(1) = 1 - w(2) - w(3);
    
    %solve for strictly l
    a32 = 1 / (6 * w(3) * c2);
    a31 = c3 - a32;
    a21 = c2;
    
    A = [0,   0,   0; 
         a21, 0,   0; 
         a31, a32, 0];
end

%% 6. data tip callba
function txt = customDataTip(~, event_obj)
    pos = event_obj.Position;
    c2 = pos(1);
    c3 = pos(2);
    
    [A, w, ~, valid] = solve_rk3_params(c2, c3);
    
    if ~valid
        txt = 'Invalid Region (Singularity)';
    else
        txt = { ...
            sprintf('Coordinates: c2=%.3f, c3=%.3f', c2, c
            sprintf('log10(Error): %.4f', event_obj.targ
            '---------------------------', ...
            'Weights (w1, w2, w3):', ...
            sprintf('[%.4f, %.4f, %.4f]', w
            'Matrix A (Lower Triangular):', ...
            sprintf('a21: %.4f', a(2,1)), ...
            sprintf('a31, a32: [%.4f, %.4f]', a(3,1),
        };
    end
end
