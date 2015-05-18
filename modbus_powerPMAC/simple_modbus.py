# coding:utf-8
#/usr/bin/env python

__author__ = 'XingHua'

import sys
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp

logger = modbus_tk.utils.create_logger("console")

if __name__ == "__main__":
    try:
        # 连接MODBUS TCP从机
        master = modbus_tcp.TcpMaster(host="192.168.14.200")
        master.set_timeout(5.0)
        logger.info("connected")
        # 读保持寄存器
        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 16))
        # 读输入寄存器
        logger.info(master.execute(1, cst.READ_INPUT_REGISTERS, 0, 16))
        # 读线圈寄存器
        logger.info(master.execute(1, cst.READ_COILS, 0, 16))
        # 读离散输入寄存器
        logger.info(master.execute(1, cst.READ_DISCRETE_INPUTS, 0, 16))
        # 单个读写寄存器操作
        # 写寄存器地址为0的保持寄存器
        logger.info(master.execute(1, cst.WRITE_SINGLE_REGISTER, 0, output_value=21))
        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 1))
        # 写寄存器地址为0的线圈寄存器，写入内容为0（位操作）
        logger.info(master.execute(1, cst.WRITE_SINGLE_COIL, 0, output_value=0))
        logger.info(master.execute(1, cst.READ_COILS, 0, 1))
        # 多个寄存器读写操作
        # 写寄存器起始地址为0的保持寄存器，操作寄存器个数为4
        logger.info(master.execute(1, cst.WRITE_MULTIPLE_REGISTERS, 0, output_value=[20, 21, 22, 23]))
        logger.info(master.execute(1, cst.READ_HOLDING_REGISTERS, 0, 4))
        # 写寄存器起始地址为0的线圈寄存器
        logger.info(master.execute(1, cst.WRITE_MULTIPLE_COILS, 0, output_value=[0, 0, 0, 0]))
        logger.info(master.execute(1, cst.READ_COILS, 0, 4))
    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))
