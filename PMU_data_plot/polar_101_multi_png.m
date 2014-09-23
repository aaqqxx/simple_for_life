clear;  clc;  tic;   % 取待测光束经过系统后的光强信号。
I(1:19, 1:262144) = 0; I0(1:512, 1:512) = 0;  I01(1, 262144) = 0;  A(1:19, 1:4) = 0;
I0 = imread('test1.png'); I01 = reshape(I0,1,262144); I(1,:) = I01;        % 读第一个波片位置的光强数据。
I_ophir=load('test1.txt'); I_ophir=sum(I_ophir); I(1,:) = I(1,:)./I_ophir; % 对第一个光强，用OPHIR数据校正。
I0 = imread('test2.png'); I01 = reshape(I0,1,262144); I(2,:) = I01;
I_ophir=load('test2.txt'); I_ophir=sum(I_ophir); I(2,:) = I(2,:)./I_ophir;
I0 = imread('test3.png'); I01 = reshape(I0,1,262144); I(3,:) = I01;
I_ophir=load('test3.txt'); I_ophir=sum(I_ophir); I(3,:) = I(3,:)./I_ophir;
I0 = imread('test4.png'); I01 = reshape(I0,1,262144); I(4,:) = I01;
I_ophir=load('test4.txt'); I_ophir=sum(I_ophir); I(4,:) = I(4,:)./I_ophir;
I0 = imread('test5.png'); I01 = reshape(I0,1,262144); I(5,:) = I01;
I_ophir=load('test5.txt'); I_ophir=sum(I_ophir); I(5,:) = I(5,:)./I_ophir;
I0 = imread('test6.png'); I01 = reshape(I0,1,262144); I(6,:) = I01;
I_ophir=load('test6.txt'); I_ophir=sum(I_ophir); I(6,:) = I(6,:)./I_ophir;
I0 = imread('test7.png'); I01 = reshape(I0,1,262144); I(7,:) = I01;
I_ophir=load('test7.txt'); I_ophir=sum(I_ophir); I(7,:) = I(7,:)./I_ophir;
I0 = imread('test8.png'); I01 = reshape(I0,1,262144); I(8,:) = I01;
I_ophir=load('test8.txt'); I_ophir=sum(I_ophir); I(8,:) = I(8,:)./I_ophir;
I0 = imread('test9.png'); I01 = reshape(I0,1,262144); I(9,:) = I01;
I_ophir=load('test9.txt'); I_ophir=sum(I_ophir); I(9,:) = I(9,:)./I_ophir;
I0 = imread('test10.png'); I01 = reshape(I0,1,262144); I(10,:) = I01;
I_ophir=load('test10.txt'); I_ophir=sum(I_ophir); I(10,:) = I(10,:)./I_ophir;
I0 = imread('test11.png'); I01 = reshape(I0,1,262144); I(11,:) = I01;
I_ophir=load('test11.txt'); I_ophir=sum(I_ophir); I(11,:) = I(11,:)./I_ophir;
I0 = imread('test12.png'); I01 = reshape(I0,1,262144); I(12,:) = I01;
I_ophir=load('test12.txt'); I_ophir=sum(I_ophir); I(12,:) = I(12,:)./I_ophir;
I0 = imread('test13.png'); I01 = reshape(I0,1,262144); I(13,:) = I01;
I_ophir=load('test13.txt'); I_ophir=sum(I_ophir); I(13,:) = I(13,:)./I_ophir;
I0 = imread('test14.png'); I01 = reshape(I0,1,262144); I(14,:) = I01;
I_ophir=load('test14.txt'); I_ophir=sum(I_ophir); I(14,:) = I(14,:)./I_ophir;
I0 = imread('test15.png'); I01 = reshape(I0,1,262144); I(15,:) = I01;
I_ophir=load('test15.txt'); I_ophir=sum(I_ophir); I(15,:) = I(15,:)./I_ophir;
I0 = imread('test16.png'); I01 = reshape(I0,1,262144); I(16,:) = I01;
I_ophir=load('test16.txt'); I_ophir=sum(I_ophir); I(16,:) = I(16,:)./I_ophir;
I0 = imread('test17.png'); I01 = reshape(I0,1,262144); I(17,:) = I01;
I_ophir=load('test17.txt'); I_ophir=sum(I_ophir); I(17,:) = I(17,:)./I_ophir;
I0 = imread('test18.png'); I01 = reshape(I0,1,262144); I(18,:) = I01;
I_ophir=load('test18.txt'); I_ophir=sum(I_ophir); I(18,:) = I(18,:)./I_ophir;
I0 = imread('test19.png'); I01 = reshape(I0,1,262144); I(19,:) = I01;
I_ophir=load('test19.txt'); I_ophir=sum(I_ophir); I(19,:) = I(19,:)./I_ophir;
%I=[1.9998 1.5867067 1.0301477 1.24995 1.8828456 1.8828456 1.24995 1.0301477 1.5867067 1.9998 1.5867067 1.0301477 1.24995 1.8828456 1.8828456 1.24995 1.0301477 1.5867067 1.9998]';
% I_ophir = [0.38 0.35 0.37 0.38 0.38 0.40 0.35 0.44 0.35 0.32 0.34 0.35 0.31 0.38 0.34 0.41 0.32 0.39 0.35 ]';
% for i = 1:19
%     I(i,:) = I(i,:)./I_ophir(i);
% end
% 定义系统矩阵A(19,4)，或者通过标定得到。
alpha  = 0 ./180*pi;  theta0 = 0 ./180*pi;  delta = 90 ./180*pi;           % 检偏器角度 % 波片初始角度% 波片光程差
p = 10000;  q = (p-1)/(p+1);  r = 2*sqrt(p)/(p+1);                         % 检偏器消光比
for k = 1:19
    theta = (k-1)*20/180*pi+theta0;
    A(k,:)=[1;
        q.*(cos(2.*alpha).*(cos(2.*theta).^2+sin(2.*theta).^2.*cos(delta))+sin(2.*alpha).*sin(2.*theta).*cos(2.*theta).*(1-cos(delta)));
        q.*(cos(2.*alpha).*sin(2.*theta).*cos(2.*theta).*(1-cos(delta))+sin(2.*alpha).*(sin(2.*theta).^2+cos(2.*theta).^2.*cos(delta)));
        q.*(sin(2.*alpha).*cos(2.*theta)-cos(2.*alpha).*sin(2.*theta)).*sin(delta)]';
end;
% 计算斯托克斯参数S。
S = A\I ;
S01 = S(1,:); S02 = reshape(S01,512,512)';            % 将SO从S中分离出来，并从一维调整到二维
S11 = S(2,:); S12 = reshape(S11,512,512)';
S21 = S(3,:); S22 = reshape(S21,512,512)';
S31 = S(4,:); S32 = reshape(S31,512,512)';
S0 = S02./S02;  S1 = S12./S02;  S2 = S22./S02;  S3 = S32./S02;
RSP_H = 0.5.*(1+S1./S0); RSP_V = 0.5.*(1-S1./S0);  DOP = sqrt(S1.*S1+S2.*S2+S3.*S3)./S0;
% 显示
figure, colormap('default');
subplot(2,2,1); imagesc(S0); title('S0'); colorbar; caxis([-1,1]);
subplot(2,2,2); imagesc(S1); title('S1'); colorbar; caxis([-1,1]);
subplot(2,2,3); imagesc(S2); title('S2'); colorbar; caxis([-1,1]); 
subplot(2,2,4); imagesc(S3); title('S3'); colorbar; caxis([-1,1]);
figure, colormap('default');
subplot(2,2,1); imagesc(RSP_H); title('RSP_H'); colorbar; caxis([-1,1]);
subplot(2,2,2); imagesc(RSP_V); title('RSP_V'); colorbar; caxis([-1,1]);
subplot(2,2,3); imagesc(DOP); title('DOP'); colorbar; caxis([-1,1]);
toc;