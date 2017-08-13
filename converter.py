import os, time, re, json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from table_def import CP, Compnd, Block


engine = create_engine('sqlite:///iccPrint.db', echo=False)


# create a Session
Session = sessionmaker(bind=engine)
session = Session()

start_time = time.time()

parameterDict = {"COMPND": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "ON", "INITON", "CINHIB", "GR1DV1", "GR1DV2", "GR1DV3", "GR1DV4", "GR1DV5", "GR1DV6", "GR1DV7", "GR1DV8", "GR2DV1", "GR2DV2", "GR2DV3", "GR2DV4", "GR2DV5", "GR2DV6", "GR2DV7", "GR2DV8", "GR3DV1", "GR3DV2", "GR3DV3", "GR3DV4", "GR3DV5", "GR3DV6", "GR3DV7", "GR3DV8", "LOOPID"], "STA": ["NAME", "TYPE", "DESCRP", "DV1", "DV2", "DV3", "DV4", "DV5", "DV6", "DV7", "DV8", "DV9", "DV10", "DV11", "DV12", "DV13", "DV14", "DV15", "DV16", "GR4", "GR5", "GR6", "GR7", "GR8", "CFGOPT", "CKPOPT", "AUTCKP", "INHPRT", "INITTE", "RESVL1", "RESVL2", "RESVL3", "RESVL4", "RESVL5", "RESVL6", "RESVL7", "RESVL8"], "ECBP": ["NAME", "TYPE", "DESCRP", "NRBUS", "BUSOPT", "BUSTYP", "PIOWDT", "MPOLL", "FIBER", "BADALM"], "ECB5": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "EXTYPE", "FSENAB", "FSDLAY", "BUSWDS", "FPM05", "FSMM05", "FSDM05", "SMM05", "P09M05", "P10M05", "P11M05", "P12M05", "P13M05", "P14M05", "P15M05", "P16M05", "FPE05", "FSME05", "FSDE05", "SME05", "P09E05", "P10E05", "P11E05", "P12E05", "P13E05", "P14E05", "P15E05", "P16E05"], "ECB1": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "EXTYPE", "FSENAB", "FSDLAY", "BUSWDS", "RES01", "ROC1", "ROC2", "ROC3", "ROC4", "ROC5", "ROC6", "ROC7", "ROC8", "ROC9", "ROC10", "ROC11", "ROC12", "ROC13", "ROC14", "ROC15", "ROC16"], "CALCA": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "RI01", "RI02", "RI03", "RI04", "RI05", "RI06", "RI07", "RI08", "BI01", "BI02", "BI03", "BI04", "BI05", "BI06", "BI07", "BI08", "BI09", "BI10", "BI11", "BI12", "BI13", "BI14", "BI15", "BI16", "II01", "II02", "LI01", "LI02", "MA", "INITMA", "TIMINI", "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "STEP01", "STEP02", "STEP03", "STEP04", "STEP05", "STEP06", "STEP07", "STEP08", "STEP09", "STEP10", "STEP11", "STEP12", "STEP13", "STEP14", "STEP15", "STEP16", "STEP17", "STEP18", "STEP19", "STEP20", "STEP21", "STEP22", "STEP23", "STEP24", "STEP25", "STEP26", "STEP27", "STEP28", "STEP29", "STEP30", "STEP31", "STEP32", "STEP33", "STEP34", "STEP35", "STEP36", "STEP37", "STEP38", "STEP39", "STEP40", "STEP41", "STEP42", "STEP43", "STEP44", "STEP45", "STEP46", "STEP47", "STEP48", "STEP49", "STEP50"], "AIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "PNT_NO", "SCI", "HSCO1", "LSCO1", "DELTO1", "EO1", "OSV", "EXTBLK", "MA", "INITMA", "BADOPT", "LASTGV", "INHOPT", "INHIB", "INHALM", "MANALM", "MTRF", "FLOP", "FTIM", "XREFOP", "XREFIN", "KSCALE", "BSCALE", "BAO", "BAT", "BAP", "BAG", "ORAO", "ORAT", "ORAP", "ORAG", "HLOP", "ANM", "HAL", "HAT", "LAL", "LAT", "HLDB", "HLPR", "HLGP", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "PROPT", "MEAS", "AMRTIN", "NASTDB", "NASOPT"], "PIDA": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "NLNBLK", "SPT", "SPCLMP", "SPHLIM", "SPLLIM", "STRKOP", "SPROPT", "SPRATE", "SPTARG", "SPRAMP", "RSP", "LR", "INITLR", "LOCSP", "LOCSW", "REMSW", "MODOPT", "INCOPT", "PBAND", "INT", "DERIV", "KD", "SPLLAG", "DTIME", "FILTER", "NONLOP", "HZONE", "LZONE", "KZONE", "SPLCOP", "SPLRDY", "TSAMPL", "BIAS", "HSCI2", "LSCI2", "DELTI2", "EI2", "BBIAS", "KBIAS", "BTRKOP", "MULTIN", "HSCIN", "LSCIN", "EIN", "HSCO1", "LSCO1", "DELTO1", "EO1", "OSV", "HOLIM", "LOLIM", "LIMOPT", "MCLOPT", "BATCHO", "PRLOAD", "TRACK", "TRKENL", "HOLD", "PRIBLK", "INITI", "BCALCI", "FBK", "MA", "INITMA", "MANFS", "MBADOP", "CEOPT", "PROPT", "MANSW", "AUTSW", "MANALM", "INHOPT", "INHIB", "INHALM", "MEASNM", "MALOPT", "MEASHL", "MEASHT", "MEASLL", "MEASLT", "MEASDB", "MEASPR", "MEASGR", "DALOPT", "DEVTIM", "HDALIM", "HDATXT", "LDALIM", "LDATXT", "DEVADB", "DEVPRI", "DEVGRP", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "OALOPT", "OUTNM", "HOALIM", "HOATXT", "LOALIM", "LOATXT", "OUTADB", "OUTPRI", "OUTGRP", "FLBOPT", "INITSE", "SUPGRP", "SUPOPT", "AMRTIN", "NASTDB", "NASOPT", "PRITIM", "BAO", "BAT", "BAP", "BAG"], "CHARC": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "EXTOPT", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PRIBLK", "BCALCI", "PROPT", "EROPT", "STPOPT", "HSCO1", "LSCO1", "DELTO1", "EO1", "STARTP", "ENDP", "X_1", "Y_1", "X_2", "Y_2", "X_3", "Y_3", "X_4", "Y_4", "X_5", "Y_5", "X_6", "Y_6", "X_7", "Y_7", "X_8", "Y_8", "X_9", "Y_9", "X_10", "Y_10", "X_11", "Y_11", "X_12", "Y_12", "X_13", "Y_13", "X_14", "Y_14", "X_15", "Y_15", "X_16", "Y_16", "X_17", "Y_17", "X_18", "Y_18", "X_19", "Y_19", "X_20", "Y_20", "X_21", "Y_21", "MA", "INITMA", "INHOPT", "INHIB", "ORAO", "ORAT", "ORAP", "ORAG", "AMRTIN", "PRITIM"], "AOUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "PNT_NO", "SCO", "ATC", "PROPT", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "MEROPT", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "OSV", "BIAS", "MSCALE", "HSCI2", "LSCI2", "DELTI2", "EI2", "BEROPT", "BTRKOP", "MA", "INITMA", "AUTSW", "MANSW", "MANFS", "MBADOP", "MCLOPT", "PRIBLK", "INHOPT", "INHIB", "BTIME", "BAO", "BAT", "BAP", "BAG", "FLBOPT", "INITSE", "SUPGRP", "SUPOPT", "AMRTIN", "PRITIM"], "OUTSEL": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "SELOPT", "INP1", "INP2", "MA", "HSCI1", "LSCI1", "DELTI1", "EI1", "HSCI2", "LSCI2", "DELTI2", "EI2", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "INITMA", "MCLOPT", "EROPT", "PRIBLK", "INITI", "BCALCI", "PRITIM"], "BIAS": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "KMEAS", "BMEAS", "BIAS", "HSCI2", "LSCI2", "DELTI2", "EI2", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "OSV", "MA", "INITMA", "MANFS", "MBADOP", "MANSW", "AUTSW", "MCLOPT", "CEOPT", "HOLD", "PRIBLK", "INITI", "BCALCI", "LR", "INITLR", "LOCSP", "LOCSW", "REMSW", "RBIAS", "KBIAS", "BBIAS", "BTRKOP", "BTIME", "MANALM", "INHOPT", "INHIB", "INHALM", "MEASNM", "MALOPT", "MEASHL", "MEASHT", "MEASLL", "MEASLT", "MEASDB", "MEASPR", "MEASGR", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "AMRTIN", "NASTDB", "NASOPT", "PRITIM", "BAO", "BAT", "BAP", "BAG", "OUTNM", "UNCLMP"], "LLAG": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "LLOPT", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "LGAIN", "LAGTIM", "LAG2", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "BIAS", "HSCI2", "LSCI2", "DELTI2", "EI2", "MA", "INITMA", "MCLOPT", "FOLLOW"], "SWCH": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "PROPT", "EROPT", "INP1", "HSCI1", "LSCI1", "DELTI1", "EI1", "INP2", "HSCI2", "LSCI2", "DELTI2", "EI2", "TOGGLE", "HSCO1", "LSCO1", "DELTO1", "EO1", "MA", "INITMA", "BTIME1", "BTIME2", "PRIBLK", "INITI", "BCALCI", "PRITIM"], "LOGIC": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "BI01", "BI02", "BI03", "BI04", "BI05", "BI06", "BI07", "BI08", "BI09", "BI10", "BI11", "BI12", "BI13", "BI14", "BI15", "BI16", "RI01", "RI02", "LI01", "MA", "INITMA", "TIMINI", "M01", "M02", "M03", "M04", "M05", "STEP01", "STEP02", "STEP03", "STEP04", "STEP05", "STEP06", "STEP07", "STEP08", "STEP09", "STEP10", "STEP11", "STEP12", "STEP13", "STEP14", "STEP15"], "STALM": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IN", "SAP", "SAG", "MA", "INITMA", "INHOPT", "INHIB", "INHALM", "BAO", "BAT", "BAP", "BAG", "PNM", "SATXT", "RTNTXT", "AMRTIN"], "LIM": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "EROPT", "PRIBLK", "INITI", "BCALCI", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "MA", "INITMA", "MCLOPT", "FOLLOW", "ROCOPT", "ROCLIM", "HSCI2", "LSCI2", "DELTI2", "EI2", "KSCALE", "PRITIM"], "MCOUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "OUTMSK", "GRPNUM", "INVOPT", "PROPT", "IN_1", "EROP1", "IN_2", "EROP2", "IN_3", "EROP3", "IN_4", "EROP4", "IN_5", "EROP5", "IN_6", "EROP6", "IN_7", "EROP7", "IN_8", "EROP8", "IN_9", "EROP9", "IN_10", "EROP10", "IN_11", "EROP11", "IN_12", "EROP12", "IN_13", "EROP13", "IN_14", "EROP14", "IN_15", "EROP15", "IN_16", "EROP16", "MA", "INITMA", "MANFS"], "CIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "PNT_NO", "ANM", "NM0", "NM1", "IVO", "MA", "INITMA", "INHOPT", "INHIB", "INHALM", "INVALM", "MANALM", "SAO", "SAP", "SAG", "BAO", "BAT", "BAP", "BAG", "SCOPT", "SCGRP", "SCTXT0", "SCTXT1", "PROPT", "IN", "AMRTIN", "NASTDB", "NASOPT"], "ALMPRI": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "PR_IN1", "PR_IN2", "PR_IN3", "PR_IN4", "PR_IN5", "MA", "INITMA"], "GDEV": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "IP_FBM", "LM1_PT", "LM2_PT", "OP_FBM", "CO1_PT", "CO2_PT", "AVLLM1", "AVLLM2", "TOC", "DSRTRK", "ZDSOVR", "AUTDSR", "MANDSR", "INTDSR", "HLDDSR", "DSR_RB", "HLD", "INTLCK", "DISABL", "MA", "INITMA", "MANSW", "AUTSW", "MANFS", "SDWNOP", "INHOPT", "INHIB", "INHALM", "ANM", "BAT", "BAP", "BAG", "SAP", "SAG", "IGNLM1", "IGNLM2", "DEVLM1", "DEVLM2", "INVLMT", "INVCO1", "INVCO2", "PLSOPT", "PLSTIM", "STAT1", "STAT2", "STAT3", "STAT4", "MM1", "MM2", "MM3", "MM4", "MODE1", "MODE2", "MODE3", "MODE4", "MODE5", "USERL1", "USERL2", "AMRTIN", "INITI"], "MCIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "CINMSK", "GRPNUM", "IVO_1", "IVO_2", "IVO_3", "IVO_4", "IVO_5", "IVO_6", "IVO_7", "IVO_8", "IVO_9", "IVO_10", "IVO_11", "IVO_12", "IVO_13", "IVO_14", "IVO_15", "IVO_16", "IVO_17", "IVO_18", "IVO_19", "IVO_20", "IVO_21", "IVO_22", "IVO_23", "IVO_24", "IVO_25", "IVO_26", "IVO_27", "IVO_28", "IVO_29", "IVO_30", "IVO_31", "IVO_32", "MA", "INITMA", "BCDOP", "NUMBIT", "HSCO1", "LSCO1", "DELTO1", "EO1", "DPLOC", "PROPT", "INPUTS", "II01", "II02"], "ACCUM": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "MTRFAC", "SET", "PRESET", "CLEAR", "HOLD", "HSCO1", "LSCO1", "DELTO1", "EO1", "INITCL", "MA", "INITMA", "CEOPT", "PCNTOP", "INHOPT", "INHIB", "INHALM", "OUTNM", "HAOPT", "HABLIM", "HABTXT", "ABSPRI", "ABSGRP", "HHAOPT", "HHALIM", "HHATXT", "HHAPRI", "HHAGRP", "AMRTIN"], "SIGSEL": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "NUMINP", "BNDX", "PROPT", "EROPT", "INP1", "HSCI1", "LSCI1", "DELTI1", "EI1", "BYPAS1", "INP2", "HSCI2", "LSCI2", "DELTI2", "EI2", "BYPAS2", "INP3", "HSCI3", "LSCI3", "DELTI3", "EI3", "BYPAS3", "INP4", "HSCI4", "LSCI4", "DELTI4", "EI4", "BYPAS4", "INP5", "HSCI5", "LSCI5", "DELTI5", "EI5", "BYPAS5", "INP6", "HSCI6", "LSCI6", "DELTI6", "EI6", "BYPAS6", "INP7", "HSCI7", "LSCI7", "DELTI7", "EI7", "BYPAS7", "INP8", "HSCI8", "LSCI8", "DELTI8", "EI8", "BYPAS8", "CASNDX", "CASINP", "HSCIC", "LSCIC", "DELTIC", "EIC", "HSCO1", "LSCO1", "DELTO1", "EO1", "MA", "INITMA", "SELOPT"], "DGAP": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "SPT", "MODOPT", "GAP", "GAPDB", "HSCI2", "LSCI2", "DELTI2", "EI2", "MA", "INITMA", "MBADOP", "MANSW", "AUTSW", "CEOPT", "HOLD", "INITI", "LR", "INITLR", "LOCSP", "LOCSW", "REMSW", "RSP", "STRKOP", "MANALM", "INHOPT", "INHIB", "INHALM", "MEASNM", "MALOPT", "MEASHL", "MEASHT", "MEASLL", "MEASLT", "MEASDB", "MEASPR", "MEASGR", "DALOPT", "HDALIM", "HDATXT", "LDALIM", "LDATXT", "DEVADB", "DEVPRI", "DEVGRP", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "AMRTIN", "NASTDB", "NASOPT"], "REALM": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "MEASNM", "HSCI1", "LSCI1", "DELTI1", "EI1", "HLAOPT", "HABLIM", "HABTXT", "LABLIM", "LABTXT", "ABSDB", "ABSPRI", "ABSGRP", "ABSRAL", "ABSINC", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "DALOPT", "SETPT", "HDALIM", "HDATXT", "LDALIM", "LDATXT", "DEVADB", "DEVPRI", "DEVGRP", "DEVRAL", "DEVINC", "ROCOPT", "ROCLIM", "HSCI2", "LSCI2", "DELTI2", "EI2", "KSCALE", "ROCTIM", "ROCTXT", "ROCPRI", "ROCGRP", "MA", "INITMA", "INHOPT", "INHIB", "INHALM", "AMRTIN", "NASTDB", "NASOPT"], "RATIO": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "RATIO", "HSCI2", "LSCI2", "DELTI2", "EI2", "KSCALE", "BSCALE", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "OSV", "MA", "INITMA", "MANFS", "MBADOP", "MANSW", "AUTSW", "MCLOPT", "CEOPT", "HOLD", "PRIBLK", "INITI", "BCALCI", "LR", "INITLR", "LOCSP", "LOCSW", "REMSW", "REMRAT", "RTRKOP", "MANALM", "INHOPT", "INHIB", "INHALM", "MEASNM", "MALOPT", "MEASHL", "MEASHT", "MEASLL", "MEASLT", "MEASDB", "MEASPR", "MEASGR", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "FLBOPT", "INITSE", "SUPGRP", "SUPOPT", "AMRTIN", "NASTDB", "NASOPT", "PRITIM", "BAO", "BAT", "BAP", "BAG", "OUTNM"], "BLNALM": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IN_1", "IVO_1", "NM0_1", "NM1_1", "ANM_1", "SAO_1", "IN_2", "IVO_2", "NM0_2", "NM1_2", "ANM_2", "SAO_2", "IN_3", "IVO_3", "NM0_3", "NM1_3", "ANM_3", "SAO_3", "IN_4", "IVO_4", "NM0_4", "NM1_4", "ANM_4", "SAO_4", "IN_5", "IVO_5", "NM0_5", "NM1_5", "ANM_5", "SAO_5", "IN_6", "IVO_6", "NM0_6", "NM1_6", "ANM_6", "SAO_6", "IN_7", "IVO_7", "NM0_7", "NM1_7", "ANM_7", "SAO_7", "IN_8", "IVO_8", "NM0_8", "NM1_8", "ANM_8", "SAO_8", "INHOPT", "INHIB", "INHALM", "SAG_1", "SAP_1", "SAG_2", "SAP_2", "SAG_3", "SAP_3", "SAG_4", "SAP_4", "SAG_5", "SAP_5", "SAG_6", "SAP_6", "SAG_7", "SAP_7", "SAG_8", "SAP_8", "AMRTIN"], "AINR": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "IOMIDR", "DEVLIM", "PNT_NO", "SCI", "HSCO1", "LSCO1", "DELTO1", "EO1", "OSV", "EXTBLK", "MA", "INITMA", "BADOPT", "LASTGV", "INHOPT", "INHIB", "INHALM", "MANALM", "MTRF", "FLOP", "FTIM", "XREFOP", "XREFIN", "KSCALE", "BSCALE", "BAO", "BAT", "BAP", "BAG", "ORAO", "ORAT", "ORAP", "ORAG", "HLOP", "ANM", "HAL", "HAT", "LAL", "LAT", "HLDB", "HLPR", "HLGP", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "PROPT", "SELREQ", "MEAS_P", "MEAS_S", "MEAS", "AMRTIN", "NASTDB", "NASOPT"], "AOUTR": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "IOMIDR", "PNT_NO", "SCO", "ATC", "PROPT", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "MEROPT", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "OSV", "BIAS", "MSCALE", "HSCI2", "LSCI2", "DELTI2", "EI2", "BEROPT", "BTRKOP", "MA", "INITMA", "AUTSW", "MANSW", "MANFS", "MBADOP", "MCLOPT", "PRIBLK", "INHOPT", "INHIB", "BTIME", "BAO", "BAT", "BAP", "BAG", "FLBOPT", "INITSE", "SUPGRP", "SUPOPT", "AMRTIN", "PRITIM"], "MON": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MA", "RSTMA", "ACTIVE", "RSTACT", "ACTPAT", "INHIB", "INHOPT", "HSCI1", "LSCI1", "DELTI1", "EI1", "BI0001", "BI0002", "BI0003", "BI0004", "BI0005", "BI0006", "BI0007", "BI0008", "BI0009", "BI0010", "BI0011", "BI0012", "BI0013", "BI0014", "BI0015", "BI0016", "BI0017", "BI0018", "BI0019", "BI0020", "BI0021", "BI0022", "BI0023", "BI0024", "BO0001", "BO0002", "BO0003", "BO0004", "BO0005", "BO0006", "BO0007", "BO0008", "BO0009", "BO0010", "BO0011", "BO0012", "BO0013", "BO0014", "BO0015", "BO0016", "II0001", "II0002", "II0003", "II0004", "II0005", "II0006", "II0007", "II0008", "RI0001", "RI0002", "RI0003", "RI0004", "RI0005", "RI0006", "RI0007", "RI0008", "RI0009", "RI0010", "RI0011", "RI0012", "RI0013", "RI0014", "RI0015", "OP_OPT", "OP_PRI", "OP_GRP", "OP_TXT", "TRPBAD", "CSPACE"], "IND": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MA", "RSTMA", "ACTIVE", "RSTACT", "INHIB", "INHOPT", "BPCSTM", "HSCI1", "LSCI1", "DELTI1", "EI1", "HSCO1", "LSCO1", "DELTO1", "EO1", "MSGGR1", "MSGGR2", "MSGGR3", "MSGGR4", "BI0001", "BI0002", "BI0003", "BI0004", "BI0005", "BI0006", "BI0007", "BI0008", "BI0009", "BI0010", "BI0011", "BI0012", "BI0013", "BI0014", "BI0015", "BI0016", "BI0017", "BI0018", "BI0019", "BI0020", "BI0021", "BI0022", "BI0023", "BI0024", "BO0001", "BO0002", "BO0003", "BO0004", "BO0005", "BO0006", "BO0007", "BO0008", "BO0009", "BO0010", "BO0011", "BO0012", "BO0013", "BO0014", "BO0015", "BO0016", "II0001", "II0002", "II0003", "II0004", "II0005", "II0006", "II0007", "II0008", "IO0001", "IO0002", "IO0003", "IO0004", "IO0005", "RI0001", "RI0002", "RI0003", "RI0004", "RI0005", "RI0006", "RI0007", "RI0008", "RI0009", "RI0010", "RI0011", "RI0012", "RI0013", "RI0014", "RI0015", "RO0001", "RO0002", "RO0003", "RO0004", "RO0005", "RO0006", "RO0007", "RO0008", "RO0009", "RO0010", "RO0011", "RO0012", "RO0013", "RO0014", "RO0015", "SN0001", "SN0002", "SN0003", "SN0004", "SN0005", "SN0006", "SN0007", "SN0008", "SN0009", "SN0010", "OP_OPT", "OP_PRI", "OP_GRP", "OP_TXT", "CSPACE"], "DEP": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MA", "RSTMA", "ACTIVE", "RSTACT", "INHIB", "INHOPT", "BPCSTM", "HSCI1", "LSCI1", "DELTI1", "EI1", "HSCO1", "LSCO1", "DELTO1", "EO1", "MSGGR1", "MSGGR2", "MSGGR3", "MSGGR4", "BI0001", "BI0002", "BI0003", "BI0004", "BI0005", "BI0006", "BI0007", "BI0008", "BI0009", "BI0010", "BI0011", "BI0012", "BI0013", "BI0014", "BI0015", "BI0016", "BI0017", "BI0018", "BI0019", "BI0020", "BI0021", "BI0022", "BI0023", "BI0024", "BO0001", "BO0002", "BO0003", "BO0004", "BO0005", "BO0006", "BO0007", "BO0008", "BO0009", "BO0010", "BO0011", "BO0012", "BO0013", "BO0014", "BO0015", "BO0016", "II0001", "II0002", "II0003", "II0004", "II0005", "II0006", "II0007", "II0008", "IO0001", "IO0002", "IO0003", "IO0004", "IO0005", "RI0001", "RI0002", "RI0003", "RI0004", "RI0005", "RI0006", "RI0007", "RI0008", "RI0009", "RI0010", "RI0011", "RI0012", "RI0013", "RI0014", "RI0015", "RO0001", "RO0002", "RO0003", "RO0004", "RO0005", "RO0006", "RO0007", "RO0008", "RO0009", "RO0010", "RO0011", "RO0012", "RO0013", "RO0014", "RO0015", "SN0001", "SN0002", "SN0003", "SN0004", "SN0005", "SN0006", "SN0007", "SN0008", "SN0009", "SN0010", "OP_OPT", "OP_PRI", "OP_GRP", "OP_TXT", "CSPACE"], "REAL": ["NAME", "TYPE", "DESCRP", "VALUE", "HSCO1", "LSCO1", "EO1"], "COUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "PNT_NO", "IN", "PROPT", "EROPT", "PLSOPT", "WIDTH", "INVCO", "MA", "INITMA", "MANFS", "INHOPT", "INHIB", "BAO", "BAT", "BAP", "BAG", "AMRTIN"], "RIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "PNT_NO", "SCI", "MGAIN", "MBIAS", "HSCI1", "LSCI1", "EI1", "MA", "INITMA", "SIMOPT", "RINP", "ROCV", "UPDPER", "OSV", "BADOPT", "INHOPT", "INHIB", "INHALM", "MANALM", "FLOP", "FTIM", "BAO", "BAT", "BAP", "BAG", "ORAO", "ORAT", "ORAP", "ORAG", "HLOP", "ANM", "HAL", "HAT", "LAL", "LAT", "HLDB", "HLPR", "HLGP", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "AMRTIN", "NASTDB", "NASOPT", "LASTGV", "OOROPT"], "PAKOUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "PKCOGP", "PKCOPT", "MA", "INITMA", "AUTSW", "MANSW", "PRIBLK", "PRITIM", "RBKTIM", "IN1", "IN2", "IN3", "IN4", "IN5", "IN6", "IN7", "IN8", "IN9", "IN10", "IN11", "IN12", "IN13", "IN14", "IN15", "IN16", "IN17", "IN18", "IN19", "IN20", "IN21", "IN22", "IN23", "IN24", "IN25", "IN26", "IN27", "IN28", "IN29", "IN30", "IN31", "IN32", "PFSOPT", "PFSOUT", "SIMOPT", "UPDPER"], "ECB202": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "PORTEX", "FILEID", "FSENAB", "FSDLAY", "WDTMR", "SFILID", "SYSCFG", "SYSOPT"], "ECB201": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "PARENT", "DVNAME", "DVADDR", "DVOPTS", "PORTNO", "FILEID", "SFILID", "MANFTR", "DVTYPE", "VERNUM", "ERROPT"], "RAMP": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "RAMP", "RMPOPT", "UPDOWN", "RMPDWN", "RMPUP", "INHDWN", "INHUP", "UPRATE", "DNRATE", "HSCI1", "LSCI1", "DELTI1", "EI1", "KSCALE", "RAMPIN", "HSCO1", "LSCO1", "DELTO1", "EO1", "HOLIM", "LOLIM", "MA", "INITMA", "MCLOPT", "HOLD", "FOLLOW", "BTIME", "REPTOP"], "IOUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "SIMOPT", "IOM_ID", "PNT_NO", "INI_PT", "IIN", "EROPT", "MA", "INITMA", "AUTSW", "MANSW", "PRIBLK", "PRITIM", "SECTIM", "RBKTIM", "FSOPTN", "FSIOUT", "INHOPT", "INHIB", "BAO", "BAT", "BAP", "BAG", "AMRTIN", "UPDPER", "SETFS"], "IIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "SIMOPT", "IOM_ID", "PNT_NO", "MA", "INITMA", "IIN", "UPDPER", "INHOPT", "INHIB", "MANALM", "BAO", "BAT", "BAP", "BAG", "AMRTIN"], "ROUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "PNT_NO", "INI_PT", "EROPT", "PRIBLK", "MEAS", "SCO", "GAIN", "BIAS", "HSCO1", "LSCO1", "EO1", "MA", "INITMA", "AUTSW", "MANSW", "PRITIM", "SECTIM", "RBKTIM", "CLPOPT", "HOLIM", "LOLIM", "SIMOPT", "FSOPTN", "FSOUT", "REVOPT", "OUTOPT", "OSV", "MANFS", "MBADOP", "INHOPT", "INHIB", "BAO", "BAT", "BAP", "BAG", "AMRTIN", "UPDPER", "SETFS", "FLBOPT", "INITSE", "SUPGRP", "SUPOPT"], "BIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "PNT_NO", "MA", "INITMA", "SIMOPT", "BIN", "SELOPT", "UPDPER", "ANM", "NM0", "NM1", "IVO", "INHOPT", "INHIB", "INHALM", "INVALM", "MANALM", "SAO", "SAP", "SAG", "BAO", "BAT", "BAP", "BAG", "SCOPT", "SCGRP", "SCTXT0", "SCTXT1", "AMRTIN", "NASTDB", "NASOPT"], "BOUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "PNT_NO", "INI_PT", "EROPT", "IN", "MA", "INITMA", "AUTSW", "MANSW", "PRIBLK", "PRITIM", "SECTIM", "RBKTIM", "SIMOPT", "FSOPTN", "FSCOUT", "MANFS", "MBADOP", "INHOPT", "INHIB", "BAO", "BAT", "BAP", "BAG", "AMRTIN", "UPDPER", "SETFS"], "STRIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "SIMOPT", "IOM_ID", "PNT_NO", "MSGOPT", "MSGGRP", "UPDPER"], "PAKIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "PKINGP", "PKIOPT", "PAKCIN", "UPDPER", "SIMOPT"], "CALC": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "RI01", "HSCI1", "LSCI1", "DELTI1", "EI1", "RI02", "HSCI2", "LSCI2", "DELTI2", "EI2", "RI03", "HSCI3", "LSCI3", "DELTI3", "EI3", "RI04", "HSCI4", "LSCI4", "DELTI4", "EI4", "RI05", "HSCI5", "LSCI5", "DELTI5", "EI5", "RI06", "HSCI6", "LSCI6", "DELTI6", "EI6", "RI07", "HSCI7", "LSCI7", "DELTI7", "EI7", "RI08", "HSCI8", "LSCI8", "DELTI8", "EI8", "BI01", "BI02", "BI03", "BI04", "BI05", "BI06", "BI07", "BI08", "BI09", "BI10", "BI11", "BI12", "BI13", "BI14", "BI15", "BI16", "II01", "II02", "LI01", "LI02", "HSCO1", "LSCO1", "EO1", "HSCO2", "LSCO2", "EO2", "HSCO3", "LSCO3", "EO3", "HSCO4", "LSCO4", "EO4", "MA", "INITMA", "TIMINI", "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10", "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20", "M21", "M22", "M23", "M24", "STEP01", "STEP02", "STEP03", "STEP04", "STEP05", "STEP06", "STEP07", "STEP08", "STEP09", "STEP10", "STEP11", "STEP12", "STEP13", "STEP14", "STEP15", "STEP16", "STEP17", "STEP18", "STEP19", "STEP20", "STEP21", "STEP22", "STEP23", "STEP24", "STEP25", "STEP26", "STEP27", "STEP28", "STEP29", "STEP30", "STEP31", "STEP32", "STEP33", "STEP34", "STEP35", "STEP36", "STEP37", "STEP38", "STEP39", "STEP40", "STEP41", "STEP42", "STEP43", "STEP44", "STEP45", "STEP46", "STEP47", "STEP48", "STEP49", "STEP50"], "ECB53": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "EXTYPE", "FSENAB", "FSDLAY", "BUSWDS", "FS1D53", "FS2D53", "FS3D53", "FS4D53", "FS5D53", "FS6D53", "FS7D53", "FS8D53", "FSMM53"], "ECB2": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "EXTYPE", "FSENAB", "FSDLAY", "BUSWDS", "RES02", "FSMM02", "FS5D02", "FS6D02", "FS7D02", "FS8D02", "ROC1", "ROC2", "ROC3", "ROC4"], "MAIN": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOMOPT", "IOM_ID", "SCI_1", "HSCO1", "LSCO1", "DELTO1", "EO1_1", "OSV_1", "SCI_2", "HSCO2", "LSCO2", "DELTO2", "EO1_2", "OSV_2", "SCI_3", "HSCO3", "LSCO3", "DELTO3", "EO1_3", "OSV_3", "SCI_4", "HSCO4", "LSCO4", "DELTO4", "EO1_4", "OSV_4", "SCI_5", "HSCO5", "LSCO5", "DELTO5", "EO1_5", "OSV_5", "SCI_6", "HSCO6", "LSCO6", "DELTO6", "EO1_6", "OSV_6", "SCI_7", "HSCO7", "LSCO7", "DELTO7", "EO1_7", "OSV_7", "SCI_8", "HSCO8", "LSCO8", "DELTO8", "EO1_8", "OSV_8", "EXTBLK", "MA", "INITMA", "BADOPT", "LASTGV", "MTRF_1", "FLOP_1", "FTIM_1", "MTRF_2", "FLOP_2", "FTIM_2", "MTRF_3", "FLOP_3", "FTIM_3", "MTRF_4", "FLOP_4", "FTIM_4", "MTRF_5", "FLOP_5", "FTIM_5", "MTRF_6", "FLOP_6", "FTIM_6", "MTRF_7", "FLOP_7", "FTIM_7", "MTRF_8", "FLOP_8", "FTIM_8", "HSCO9", "LSCO9", "DELTO9", "EO1_9", "OSV_9", "FLOPTC", "FTIMTC", "XREFOP", "XREFIN", "KSCALE", "BSCALE", "OCTNUM", "PROPT", "MEAS_1", "MEAS_2", "MEAS_3", "MEAS_4", "MEAS_5", "MEAS_6", "MEAS_7", "MEAS_8"], "FBTUNE": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "PIDBLK", "PROG", "PROGLT", "PROGUT", "THRESH", "PR_FL", "LIM", "ITMAX", "ITMIN", "PBMAX", "PBMIN", "PR_TYP", "PIDRCL", "PM", "IM", "DM", "STNREQ", "STHREQ"], "EXC": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MA", "RSTMA", "ACTIVE", "RSTACT", "INHIB", "INHOPT", "BPCSTM", "HSCI1", "LSCI1", "DELTI1", "EI1", "HSCO1", "LSCO1", "DELTO1", "EO1", "MSGGR1", "MSGGR2", "MSGGR3", "MSGGR4", "BI0001", "BI0002", "BI0003", "BI0004", "BI0005", "BI0006", "BI0007", "BI0008", "BI0009", "BI0010", "BI0011", "BI0012", "BI0013", "BI0014", "BI0015", "BI0016", "BI0017", "BI0018", "BI0019", "BI0020", "BI0021", "BI0022", "BI0023", "BI0024", "BO0001", "BO0002", "BO0003", "BO0004", "BO0005", "BO0006", "BO0007", "BO0008", "BO0009", "BO0010", "BO0011", "BO0012", "BO0013", "BO0014", "BO0015", "BO0016", "II0001", "II0002", "II0003", "II0004", "II0005", "II0006", "II0007", "II0008", "IO0001", "IO0002", "IO0003", "IO0004", "IO0005", "RI0001", "RI0002", "RI0003", "RI0004", "RI0005", "RI0006", "RI0007", "RI0008", "RI0009", "RI0010", "RI0011", "RI0012", "RI0013", "RI0014", "RI0015", "RO0001", "RO0002", "RO0003", "RO0004", "RO0005", "RO0006", "RO0007", "RO0008", "RO0009", "RO0010", "RO0011", "RO0012", "RO0013", "RO0014", "RO0015", "SN0001", "SN0002", "SN0003", "SN0004", "SN0005", "SN0006", "SN0007", "SN0008", "SN0009", "SN0010", "OP_OPT", "OP_PRI", "OP_GRP", "OP_TXT", "CSPACE"], "PTC": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "SPT", "PBAND", "GAP", "HSCI2", "LSCI2", "DELTI2", "EI2", "REPTIM", "MA", "INITMA", "MBADOP", "MANSW", "AUTSW", "CEOPT", "HOLD", "INITI", "LR", "INITLR", "LOCSP", "LOCSW", "REMSW", "RSP", "STRKOP", "MANALM", "INHOPT", "INHIB", "INHALM", "MEASNM", "MALOPT", "MEASHL", "MEASHT", "MEASLL", "MEASLT", "MEASDB", "MEASPR", "MEASGR", "DALOPT", "HDALIM", "HDATXT", "LDALIM", "LDATXT", "DEVADB", "DEVPRI", "DEVGRP", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "AMRTIN", "NASTDB", "NASOPT"], "ECB210": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "IPADDR", "LMACA", "FCMCFG"], "MATH": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "RI01", "RI02", "RI03", "RI04", "RI05", "RI06", "RI07", "RI08", "MA", "INITMA", "M01", "M02", "M03", "M04", "M05", "STEP01", "STEP02", "STEP03", "STEP04", "STEP05", "STEP06", "STEP07", "STEP08", "STEP09", "STEP10", "STEP11", "STEP12", "STEP13", "STEP14", "STEP15", "STEP16", "STEP17", "STEP18", "STEP19", "STEP20"], "TIM": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MA", "RSTMA", "HSCI1", "LSCI1", "DELTI1", "EI1", "TIMR1R", "TIMR1V", "TIMR2R", "TIMR2V", "TIMR3R", "TIMR3V", "TIMR4R", "TIMR4V"], "BOOL": ["NAME", "TYPE", "DESCRP", "VALUE", "STATE0", "STATE1"], "PLSOUT": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "IOM_ID", "CO1_PT", "CO2_PT", "RBK_PT", "INI_PT", "EROPT", "IN", "PLSTIM", "MA", "INITMA", "AUTSW", "MANSW", "PRIBLK", "PRITIM", "SIMOPT"], "LONG": ["NAME", "TYPE", "DESCRP", "VALUE", "EO1"], "FFTUNE": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "PIDBLK", "PROG", "PROGLT", "PROGUT", "THRESH", "LOAD1", "HSCI1", "LSCI1", "DELTI1", "EI1", "LOAD2", "HSCI2", "LSCI2", "DELTI2", "EI2", "LOAD3", "HSCI3", "LSCI3", "DELTI3", "EI3", "LOAD4", "HSCI4", "LSCI4", "DELTI4", "EI4", "FTNREQ", "FTHREQ"], "DTIME": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "MEAS", "HSCI1", "LSCI1", "DELTI1", "EI1", "PROPT", "DTOPT", "DT", "NUMBKT", "HSCO1", "LSCO1", "DELTO1", "EO1", "MA", "INITMA", "FOLLOW", "HOLD", "CEOPT"], "ECB200": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "DEV_ID", "HWTYPE", "SWTYPE", "PORTEX", "FILEID", "FSENAB", "FSDLAY", "WDTMR", "SFILID", "SYSCFG", "SYSOPT"], "RINR": ["NAME", "TYPE", "DESCRP", "PERIOD", "PHASE", "LOOPID", "SIMOPT", "ECBOPT", "IOMID1", "IOMID2", "IOMID3", "RI1_PT", "RI2_PT", "RI3_PT", "ARBOPT", "ARBLIM", "SELOPT", "SCI", "MGAIN", "MBIAS", "HSCI1", "LSCI1", "EI1", "MA", "INITMA", "RINP", "ROCV", "UPDPER", "OSV", "BADOPT", "INHOPT", "INHIB", "INHALM", "MANALM", "FLOP", "FTIM", "BAO", "BAT", "BAP", "BAG", "ORAO", "ORAT", "ORAP", "ORAG", "HLOP", "ANM", "HAL", "HAT", "LAL", "LAT", "HLDB", "HLPR", "HLGP", "HHAOPT", "HHALIM", "HHATXT", "LLALIM", "LLATXT", "HHAPRI", "HHAGRP", "AMRTIN", "NASTDB", "NASOPT", "LASTGV", "OOROPT"]}

folder = 'all'

block_parameters = []
bname =''
btype = ''
bdata = ''
bname_set = False
btype_set = False
new_block_ready = False
newBlockData = []
clist = []
blist = []

filenameRe = r'(\d{4}[AWP]{2})_(\d{6}).txt'

def scanFiles(folder):
    """ In: folder directory 
        Out: list of file names
    """
    filenameList = []

    cwd = os.getcwd()
    os.chdir(cwd + '\\' + folder)
    cwd = os.getcwd()

    for name in os.listdir(cwd):
        match = re.search(filenameRe, name)
        if match:
            filenameList.append(match.group(0))

    return filenameList

def dataExtractor(filename):
    """ In: file
        Out: hostName, cpName, list of lines
    """
    file = open(filename)
    data = list(file)
    file.close()
    match = re.search(filenameRe, filename)

    return match.group(1), match.group(2), data

def blockPrep(data):
    nameRe = r'^NAME\s+=\s+(.*)\s$'
    typeRe = r'^\s+TYPE\s+=\s+(.*)\s$'
    bnameRe = r'^(.*):(.*)$'
    
    nameMatch = False
    typeMatch = False
    bnameMatch = False
    paramAddition =False
    newBlockData = []
    parameterList = []
    cname = ''
    bname = ''
    btype = ''
    paramNo = 1


    for line in data:
        # Found Name and Type
        if nameMatch and typeMatch:
            
            bname = nameMatch.group(1)
            bnameMatch = re.search(bnameRe, bname)
            #----------------
            # if bname == 'P104U_A13600:HS499A':
                # print (data)
                
            
            if bnameMatch:
                cname = bnameMatch.group(1)
                bname = bnameMatch.group(2)
            else:
                cname = bname


            btype = typeMatch.group(1)
            parameterList = parameterDict[btype]

            # Check the number of parameters
            if len(data) != len(parameterList):
                print ('Error-0002: data len is %d while len parmeter list is %d' %(len(data), len(parameterList)))
                print (name)
                print (data)
                print (parameterList)
                break 

            nameMatch = False
            typeMatch = False
            paramAddition =True  

            
        if not paramAddition:
            if not nameMatch:
                nameMatch = re.search(nameRe, line)
            elif not typeMatch:
                typeMatch = re.search(typeRe, line)

        else:
            paramNo += 1
            paramRe = r'^\s+%s\s+=\s+(.*)\s$' %(parameterList[paramNo])
            paramMatch = re.search(paramRe, line)
            if paramMatch:
                newBlockData.append(paramMatch.group(1))
            else:
                print  ("Error-0001: The parameter: %s not found in line %s") %(parameterList[paramNo], line)
                break
    return cname, bname, btype, newBlockData



##################################

filenameList = scanFiles(folder)



for name in filenameList:
    print ("Working with " + name)

    # --------------------------


    fileStartTime = time.time()

    # hostName, cpName, fileData = dataExtractor(name)

    match = re.search(filenameRe, name)
    hostName = match.group(1) 
    cpName = match.group(2)
    newCP = CP(cpName)

    # newBlockData = []
    newBlockReady = False

    with open (name, encoding = 'Latin-1') as file:  #encoding = 'Latin-1'
        for line in file:
            if line.strip('\n')=='END':
                newBlockReady = True
            else:
                newBlockData.append(line)

            if newBlockReady:
                cname, bname, btype, newBlockData = blockPrep(newBlockData)
                if cname not in clist:
                    clist.append(cname)
                    currentComp = Compnd(cname)
                    currentComp.cp = newCP
                    
                    
                    
                bdata = json.dumps(newBlockData)
                #print ("Block: " + bname + ' TYPE: ' + btype + ' DATA:' + bdata
                currentComp.blocks.append(Block(bname, btype, bdata))
                
                newBlockData = []
                newBlockReady = False




    
    

    # for line in fileData:
    #     if line.strip('\n')=='END':
    #         newBlockReady = True
    #     else:
    #         newBlockData.append(line)

    #     if newBlockReady:
    #         cname, bname, btype, newBlockData = blockPrep(newBlockData)
    #         if cname not in clist:
    #            	clist.append(cname)
    #            	currentComp = Compnd(cname)
    #            	currentComp.cp = newCP
            	
            	
            	
    #         bdata = pickle.dumps(newBlockData)
    #         #print ("Block: " + bname + ' TYPE: ' + btype + ' DATA:' + bdata
    #         currentComp.blocks.append(Block(bname, btype, bdata))
            
    #         newBlockData = []
    #         newBlockReady = False

    
    session.add(newCP)
    session.commit()

    print(name + " exec time: %s seconds" %(time.time() - fileStartTime))
