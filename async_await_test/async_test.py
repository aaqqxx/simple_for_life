import sys
import time

def binary(n):
    if n <= 0:
        return 1
    l = yield from binary(n - 1)
    r = yield from binary(n - 1)
    return l + 1 + r

async def abinary(n):
    if n <= 0:
        return 1
    l = await abinary(n - 1)
    r = await abinary(n - 1)
    return l + 1 + r

def timeit(func, depth, repeat):
    t0 = time.time()
    for _ in range(repeat):
        o = func(depth)
        try:
            while True:
                o.send(None)
        except StopIteration:
            pass
    t1 = time.time()
    print('{}({}) * {}: total {:.3f}s'.format(
        func.__name__, depth, repeat, t1-t0))

# timeit(binary,19,30)
# timeit(abinary,19,30)

txt='''
SMEE_DOUBLE 	ywaferVSRatio;	//Wafer到VS的y向放大倍率
SMEE_DOUBLE 	xwaferVSRatio;	//Wafer到VS的x向放大倍率  SMEE_DOUBLE  ywaferVSOffset ;	// Wafer到VS的y向偏差
SMEE_DOUBLE  xwaferVSOffset;	//Wafer到VS的x向偏差
ILMC_GRID_POSITION_RANGE_STRUCT	 grid1PositionRange;
ILMC_GRID_POSITION_RANGE_STRUCT	grid2PositionRange;
SMEE_DOUBLE	yAperture;	//VS坐标级的Y窗口最大尺寸【SIOM使用】
SMEE_DOUBLE	xAperture;	//VS坐标级的X窗口最大尺寸【SIOM使用】
SMEE_DOUBLE	blackBorderSize;	 //黑边尺寸 //应该是整机上测试的。。。
ES4A_VS_WINDOWS_STRUCT	 waferWindowInit;  //窗口初始尺寸【SIOM使用】
SMEE_DOUBLE	minSpeed;	//VS最小扫描速度【SIOM使用，需SMEE进一步解释】
SMEE_DOUBLE	maxSpeed;	//VS最大扫描速度【SIOM使用】
SMEE_DOUBLE 	xCenterOffset;	//X方向中心偏差【SIOM使用】
SMEE_DOUBLE	yCenterOffset ;	//Y方向中心偏差【SIOM使用】
ILMC_PROFILE_WIDTH_CONFIG_STRUCT  profileWidthConfig;	//计算Profile宽度尺寸的参数
ILMC_SERVO_PARAMETER_STRUCT	VSServoParameter;	//VS的伺服参数【需与SMEE讨论确定】
'''
res = txt.split()
print(len(res)),range(0,50,3)
for index in range(0,int(len(res)),3):
    print(res[index]),"\t",(res[index+1]),(res[index+2])