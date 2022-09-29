#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>


bool defined(int input) {
	return (bool)input;
}

#define Rte_Read_HwLifeCycSt_LifeCycSt Rte_Read_Idp_HwLifeCycSt_LifeCycSt
#define Rte_Read_OBD_DCY_InitiallySet_ObdNonvolStructType Rte_Read_Idp_OBD_DCY_InitiallySet_ObdNonvolStructType
#define Rte_Call_PS_NvM_BLOCK_VW_DATA_SET_NUMBER_SetRamBlockStatus Rte_Call_Idp_PS_NvM_BLOCK_VW_DATA_SET_NUMBER_SetRamBlockStatus
#define Rte_Call_PS_NvM_BLOCK_VW_DATA_SET_NUMBER_WriteBlock Rte_Call_Idp_PS_NvM_BLOCK_VW_DATA_SET_NUMBER_WriteBlock
#define Rte_Call_PS_NvM_BLOCK_VW_DATA_SET_VERSION_NUMBER_SetRamBlockStatus Rte_Call_Idp_PS_NvM_BLOCK_VW_DATA_SET_VERSION_NUMBER_SetRamBlockStatus
#define Rte_Call_PS_NvM_BLOCK_VW_DATA_SET_VERSION_NUMBER_WriteBlock Rte_Call_Idp_PS_NvM_BLOCK_VW_DATA_SET_VERSION_NUMBER_WriteBlock
#define Rte_Call_Internal_KnockOut_KnockOutCtrINT_IF Rte_Call_Idp_Internal_KnockOut_KnockOutCtrINT_IF
#define Rte_Call_Internal_KnockOut_KnockOutTmrINT_IF Rte_Call_Idp_Internal_KnockOut_KnockOutTmrINT_IF
#define Rte_Call_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_TMR_SetRamBlockStatus Rte_Call_Idp_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_TMR_SetRamBlockStatus
#define Rte_Call_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_TMR_WriteBlock Rte_Call_Idp_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_TMR_WriteBlock
#define Rte_Call_PS_NvM_BLOCK_PModeParam_SetRamBlockStatus Rte_Call_Idp_PS_NvM_BLOCK_PModeParam_SetRamBlockStatus
#define Rte_Call_PS_NvM_BLOCK_PModeParam_WriteBlock Rte_Call_Idp_PS_NvM_BLOCK_PModeParam_WriteBlock
#define Rte_Call_Event_P_MODE_SetEventStatus Rte_Call_Idp_Event_P_MODE_SetEventStatus
#define Rte_Write_Idp_Expected_model_type_PECInIf_idxCalDatAdp_VW Rte_Write_Idp_Idp_Expected_model_type_PECInIf_idxCalDatAdp_VW
#define Rte_Call_PS_NVM_BLOCK_EXPECTED_MODEL_TYPE_SetRamBlockStatus Rte_Call_Idp_PS_NVM_BLOCK_EXPECTED_MODEL_TYPE_SetRamBlockStatus
#define Rte_Call_PS_NVM_BLOCK_EXPECTED_MODEL_TYPE_WriteBlock Rte_Call_Idp_PS_NVM_BLOCK_EXPECTED_MODEL_TYPE_WriteBlock
#define Rte_Write_KnockOut_Test_KnockOutTestBit Rte_Write_Idp_KnockOut_Test_KnockOutTestBit
#define Rte_Call_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_CTR_SetRamBlockStatus Rte_Call_Idp_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_CTR_SetRamBlockStatus
#define Rte_Call_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_CTR_WriteBlock Rte_Call_Idp_PS_NvM_BLOCK_KNOCK_OUT_PARAMETER_CTR_WriteBlock
#define RTE_E_DataServices_F191_ECUHardwareNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F187_VWSparePartNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F1A3_VWECUHardwareVersionNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F189_VWApplicationSoftwareVersionNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F197_VWSystemNameOrEngineType_E_NOT_OK 1U
#define RTE_E_DataServices_x0407_VWLogicalSoftwareBlockCounterOfProgrammingAttempts_E_NOT_OK 1U
#define RTE_E_DataServices_x040F_VWLogicalSoftwareBlockLockValue_E_NOT_OK 1U
#define RTE_E_DataServices_x0410_BootloaderTPBlocksize_E_NOT_OK 1U
#define RTE_E_DataServices_F15B_FingerprintAndProgrammingDateOfLogicalSoftwareBlocks_E_NOT_OK 1U
#define RTE_E_DataServices_F18A_SystemSupplierIdentifier_E_NOT_OK 1U
#define RTE_E_DataServices_F18C_ECUSerialNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F192_SystemSupplierECUHardwareNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F194_SystemSupplierECUSoftwareNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F195_SystemSupplierECUSoftwareVersionNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F19E_AsamOdxFileIdentifier_E_NOT_OK 1U
#define RTE_E_DataServices_F1A0_VWDataSetNumberOrECUDataContainerNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F1A1_VWDataSetVersionNumber_E_NOT_OK 1U
#define RTE_E_DataServices_F1B6_System_identification_E_NOT_OK 1U
#define RTE_E_DataServices_F1B4_Technical_specifications_version_E_NOT_OK 1U
#define RTE_E_DataServices_F1AF_AUTOSAR_standard_application_software_identification_E_NOT_OK 1U
#define RTE_E_DataServices_x0102_BasicSettingsStatus_E_NOT_OK 1U
#define RTE_E_DataServices_x02B3_Response_On_Event_E_NOT_OK 1U
#define RTE_E_DataServices_x0261_OBD_Driving_Cycle_set_once_E_NOT_OK 1U
#define RTE_E_DataServices_F1DF_ECUProgrammingInformation_E_NOT_OK 1U
#define RTE_E_DataServices_F1AA_VWWorkshopSystemName_E_NOT_OK 1U
#define RTE_E_DataServices_F1AB_VWLogicalSoftwareBlockVersion_E_NOT_OK 1U
#define RTE_E_DataServices_F1A2_AsamOdxFileVersion_E_NOT_OK 1U
#define RTE_E_DataServices_x02CA_Knockout_counter_E_NOT_OK 1U
#define RTE_E_DataServices_x02CB_Knockout_timer_E_NOT_OK 1U
#define RTE_E_DataServices_x019C_Status_productionmode_E_NOT_OK 1U
#define RTE_E_DataServices_x04FC_Productionmode_deactivate_E_NOT_OK 1U
#define RTE_E_DataServices_x04FE_Productionmode_E_NOT_OK 1U
#define RTE_E_DataServices_FD00_VsEA_HardwareIdentification_CU_E_NOT_OK 1U
#define RTE_E_DataServices_FD01_VsEA_HardwareIdentification_PU_E_NOT_OK 1U
#define RTE_E_DataServices_FD02_VsEA_HardwareIdentification_FilterBoard_E_NOT_OK 1U
#define RTE_E_DataServices_FD03_VsEA_HardwareIdentification_IGBT_E_NOT_OK 1U
#define RTE_E_DataServices_FD04_VsEA_HardwareIdentification_InvCover_E_NOT_OK 1U
#define RTE_E_DataServices_FEFF_VsEA_MicrocontrollerId_E_NOT_OK 1U
#define RTE_E_DataServices_F1B8_VW_system_firmware_versions_E_NOT_OK 1U
#define RTE_E_DataServices_F1B8_VW_system_firmware_versions_DCM_E_PENDING 10U
#define RTE_E_DataServices_F182_VWApplicationDataIdentification_E_NOT_OK 1U
#define RTE_E_E2EProtectedDID_x0903_Expected_model_type_E_NOT_OK 1U
#define RTE_E_DataServices_F41C_OBD_requirements_to_which_vehicle_or_engine_is_certified_E_NOT_OK 1U
#define RTE_E_DataServices_F1F4_Bootloader_identification_E_NOT_OK 1U
#define RTE_E_DataServices_x09F3_KnockOut_test_mode_E_NOT_OK 1U
#define RTE_E_DataServices_x0448_ProgPrecond_E_NOT_OK 1U
#define RTE_E_DataServices_x02CE_OBDtype_E_NOT_OK 1U
#define RTE_E_DataServices_x02CF_OBD_class_description_E_NOT_OK 1U
#define RTE_E_DataServices_F1AD_EngineCodeLetters_E_NOT_OK 1U
#define RTE_E_NvMService_E_NOT_OK 1U
#define RTE_E_DiagnosticMonitor_E_NOT_OK 1U
#define ECU_ID_HIB              (0x00U)
#define ECU_ID_LOB              (0x51U)
#define NODE_ADDR_HIB           (0x00U)
#define NODE_ADDR_LOB           (0x7CU)
#define NUMBER_OF_SOFTWARE_BLOCKS                                       5U  /* Anzahl der logischen Softwareblocke */
#define NUMBER_OF_RECORDS_OF_BOOT_OR_APP                                1U
#define DEFAULT_INIT_VALUE                                              0x2DU /* Init value ascii '-' */
#define DID_F1A1_DATA_RANGE_LOW_TH                                      0x30U
#define DID_F1A1_DATA_RANGE_HIGH_TH                                     0x39U
#define EXPECTED_MODEL_INIT_VALUE                                       0U
#define DGP_VERSION_NUMBER                                              0x01U /* Q-LAH_80125_T2-1359 */
#define DGP_ZERO_CHAR                                                   0x30U /* Ascii char '0' */
#define DGP_ONE_CHAR                                                    0x31U /* Ascii char '1' */
#define DID_0102_BASICSETTINGSTATUS_SIZE                                1U
#define DID_0261_DRIVINGCYCLESETONCE_SIZE                               1U
#define DID_0407_VWLOGICALSWBLCNTOFPRGATT_SIZE                          ((NUMBER_OF_SOFTWARE_BLOCKS-1U) *2U)
#define DID_040F_VWLOGICALSWBLLOCKVALUE_SIZE                            2U
#define DID_F15B_FINGERPRINTANDPRGDATEOFLOGSWBL_SIZE (DID_F15A_BLOCKPGMDATE_SIZE + DID_F15A_BLOCKTESTERSERIAL_SIZE + 1U)
#define DID_0410_BLFTPBLOCK_SIZE                                        1U
#define DID_F182_VWAPPLDATAIDENTIFICATION_SIZE                          4U
#define DID_F187_VWSPAREPARTNUMBER_SIZE                                 11U
#define DID_F187_VWSPAREPARTNUMBER_FRONT_NUMBER                         3U
#define DID_F187_VWSPAREPARTNUMBER_END_NUMBER                           5U
#define DID_F189_VWSOFTWAREVERSIONNUMBER_SIZE                           4U
#define DID_F18C_ECUSERIALNUMBER_SIZE                                   20U
#define DID_F18A_VWSYSSUPIDNUM_SIZE                                     7U
#define DID_F191_VWECUHARDWARENUMBER_SIZE                               11U
#define DID_F197_VWSYSTEMNAME_SIZE                                      13U
#define DID_F19E_ASAMODXFILEIDENTIFIER_MAX_SIZE                         25U
#define DID_F19E_ASAMODXFILEIDENTIFIER_SIZE                             25U
#define F19E_ASAMODXFILEIDENTIFIER_SIZE_NONVM                           24U
#define DID_F1A0_VWDATASETNUMMBEROFECUDATACONTNUM_SIZE                  11U
#define DID_F1A1_VWDATASETVERSIONNUMBER_SIZE                            4U
#define DID_F1A2_ASAMODXFILEVERSION_SIZE                                6U
#define DID_F1A3_VWECUHARDWAREVERSIONNUMBER_SIZE                        3U
#define DID_F1AA_VWWORKSHOPSYSTEMNAME_SIZE                              5U
#define DID_F1AB_LOGICALBLOCKVERSION_SIZE                               4U
#define DID_F1AD_ENGINECODELETTERS_SIZE                                 4U
#define DID_0189_DGPVER_SIZE                                            4U
#define DID_F1AF_AUTOSARSTDAPPSWID_SIZE                                 7U
#define DID_F1AF_SFDA_CFG_SW_MAJOR_VERSION                              2U
#define DID_F1AF_SFDA_CFG_SW_MINOR_VERSION                              12U
#define DID_F1AF_SFDA_CFG_SW_PATCH_VERSION                              6U
#define DID_F1AF_SFDA_CFG_VENDOR_ID                                     1U
#define DID_F1AF_SFDA_CFG_MODULE_ID                                     55552U
#define DID_F15A_BLOCKTESTERSERIAL_SIZE                                 6U
#define DID_F15A_BLOCKPGMDATE_SIZE                                      3U
#define DID_F15A_VWCODINGREPAIRSHOPCODEORSERIALNUMBER_SIZE (DID_F15A_BLOCKTESTERSERIAL_SIZE + DID_F15A_BLOCKPGMDATE_SIZE)
#define DID_F1B4_TECHSPECVERSION_SIZE                                   26U
#define DID_F1B4_MAJOR_MINOR_TECHSPECVERSION_SIZE                       2U
#define DID_F1B6_SYSTEMIDENTIFICATION_SIZE                              4U
#define DID_F1B8_FIRMWARE_VERSION_SIZE_FULL                             21U
#define DID_F1B8_FIRMWARE_VERSION_SIZE_WITHOUT_SB                       17U
#define DID_F190_VIN_SIZE                                               17U
#define DID_F17C_VWFAZITIDENTIFICATIONSTRING_SIZE                       23U
#define DID_F192_SYS_SUPP_ECU_HW_NUM_SIZE                               21U
#define DID_F194_SYS_SUPP_ECU_SW_NUM_SIZE                               11U
#define DID_F195_SYS_SUPP_ECU_SW_VER_NUM_SIZE                           1U
#define DID_F1DF_ECUPROGINFO_SIZE                                       1U
#define DID_02CA_KNOCKOUTCOUNTER_SIZE                                   2U
#define DID_02CB_KNOCKOUTTIMER_SIZE                                     3U
#define DID_09F3_KNOCKOUTTEST_SIZE                                      1U
#define ECUKNOCKOUT_BYTE                                                0U
#define BUSKNOCKOUT_BYTE                                                1U
#define NVEMKNOCKOUT_BYTE                                               2U
#define DID_02B3_RESPONSEONEVENT_SIZE                                   1U
#define DID_FD00_VESA_HARDWAREIDENTIFICATION_CU_SIZE                    21U
#define DID_FD01_VESA_HARDWAREIDENTIFICATION_PU_SIZE                    21U
#define DID_FD02_VESA_HARDWAREIDENTIFICATION_FILTERBOARD_SIZE           21U
#define DID_FD03_VESA_HARDWAREIDENTIFICATION_IGBT_SIZE                  21U
#define DID_FD04_VESA_HARDWAREIDENTIFICATION_INVCOVER_SIZE              21U
#define DID_FEFF_VESA_MICROCONTROLLERID_SIZE                            16U
#define DID_F1F4_BOOTLOADERIDENTIFICATION_SIZE                          29U
#define DID_F1DF_ECUPROGRAMMINGINFORMATION                              0x40U
#define ADMIN_TABLE_VALIDITY_BITMASK                                    0xFFFFFF00U
#define ADMIN_TABLE_PATTERN_MASK                                        0xFFU
#define UNLOCK_STATUS_OF_PROTECTION_OF_VEHICLE_SIZE                     3U
#define F1A0_VWDATASETNUMBERORECUDATACONTAINERNUMBER_SIZE               11U
#define F1A0_MIDDLE_NUMBER_TH                                           3U
#define F1A0_PART_NUMBER_SUFFIX_TH                                      9U
#define F1A0_RANGE_LOW_TH                                               0x30U
#define F1A0_PROHIBITED_CHAR                                            0X40U
#define F1A0_SUFFIX_RANGE_LOW_TH                                        0x41U
#define F1A0_FRONT_SUFFIX_NM_RANGE_HIGH_TH                              0X5AU
#define F1A0_MIDDLE_NM_RANGE_HIGH_TH                                    0X39U
#define F1A0_SPACE_CHAR                                                 0X20U
#define NO_IOCTRL                                                       0U
#define ROUTINE_CTRLS_NOT_ACTIVE                                        0U
#define RESPONSE_ON_EVENT_NOT_ACTIVE                                    0U
#define HW_STRING_SIZE                                                  4U
#define INITIALIZE_ADAPTION_VALUE_BITMASK                               0x0FU
#define MILAGE_ARRAY_SIZE                                               3U
#define DID_02DF_MAX_LENGTH                                             516U
#define ASCII_Y_HEX                                                     0x59U
#define DID_04FC_PRODUCTIONMODE_DEACTIVATE_INIT_VALUE                   3U
#define LOCKVALUE_DEFAULT                                               (0xE803U) /* swapped */
#define X02CF_VERSION_NUMBER                                            0x01U /* Version 1 - [Q-LAH_80125_T2-1399] */
#define X02CF_OBD_CLASS                                                 0x84U
#define VERSION_SIZE              (32U)
#define PROD_DATA_ARRAY_SIZE      (32U)
#define PROD_DATA_OEM_ARRAY_SIZE  (16U)
#define F18C_ECUSERNUM_ARRAY_SIZE (32U)
#define PATTERN_ACTIVE            (0xA5U)
#define CRETA_REVISION_SIZE		 (64U)
#define HWVERS_UNKNOWN            (0U)
#define HWVERS_BPC3               (1U)
#define HWVERS_BMC2               (2U)
#define PSR_DEFAULT_SESSION      (1U)
#define PSR_NON_DEFAULT_SESSION  (10U)
#define PSR_SESSION_INIT         (0U)
#define PSR_DIAGTIMER_LIMIT_10_SEC     (2000UL)   /* 5ms *2000    = 10 000 ms = 10 sec */
#define PSR_DIAGTIMER_LIMIT_60_SEC     (12000UL)  /* 5ms *120 00 = 60 000 ms = 600 sec */
#define PSR_DIAGTIMER_LIMIT_900_SEC    (180000UL) /* 5ms *180 000 = 900 000 ms = 900 sec */
#define PSR_RESPONSE_PENDING     (1U)
#define BUSKO_TMR_THRESHOLD           (0U) /* The InternalTmr_Bus is not to be decremented at the value 0x00 [KO_397] */
#define BUSKO_TMR_MINVALUE            (15U)
#define BUSKO_TMR_INITVALUE           (15U)
#define BUSKO_DEACTIVATED             (0x3FU)
#define BUSKO_DEACTIVATED_CAN_VALUE   (0xFFU)
#define BUSKO_CTR_INITVALUE           (0U)
#define BUSKO_CTR_OVERFLOW            (254U)
#define BUSKO_TIMER_TRESHOLD          (120U) /* 500ms*120 = 60000ms = 60sec */
#define ECUKO_TMR_THRESHOLD           (0U) /* The InternalTmr_ECU is not to be decremented at the value 0x00 [KO_706] */
#define ECUKO_TMR_MINVALUE            (1U)
#define ECUKO_TMR_INITVALUE           (15U)
#define ECUKO_DEACTIVATED             (0X3FU)
#define ECUKO_CTR_INITVALUE           (0U)
#define ECUKO_CTR_OVERFLOW            (254U)
#define ECUKO_TIMER_TRESHOLD          (120U)    /* 500ms*120 = 60000ms = 60sec */
#define NO_NM_COMMUNICATION_REASON     0U
#define KNOCKOUT_CYCLE_CTR_INIT       (0U)
#define KNOCKOUT_TESTBIT_ACTIVATED              (0x01U)
#define KNOCKOUT_TESTBIT_VETO                   (0x02U)
#define KNOCKOUT_TESTBIT_ACTIVATED_AND_VETO     (0x03U)
#define KNOCKOUT_TESTBIT_SUPPRESS_VETO          (0x04U)
#define FUNCTION_NOT_TRIGGERED                  (0x00U)
#define VETO_ACTIVE                             (0x01U)
#define FUNCTION_TRIGGERED                      (0x02U)
#define FUNCTION_DEACTIVATED                    (0x03U)
#define PSR_FLASH_UPDATE_FLAG_MASK        (0x00000100U)
#define PSR_ECUM_SBCSLEEPREQTIMEOUT    (500000000UL)
#define UNKNOWN_PERIPHERIE_WAKE_UP 0x00u
#define BUS_WAKE_UP                0x01u
#define KL15_WAKE_UP               0x02u
#define LE_AKTIV_WAKE_UP           0x04u
#define NMH_ACT_TMIN_NO_200MS    40U   /* 5ms * 40 = 200ms */
#define PSR_PRTMR_CYCLETIME      5U     /* [ms] */
#define EMSTATOR_TIMER_INACTIVE        0U
#define EMSTATOR_TIMER_ACTIVE          1U
#define EMSTATOR_TIMER_ELAPSED        2U
#define MAX_LENGTH_PRECOND_LIST     9U
#define SERV_PRECOND_ENGINE_SPEED                1U  /* Prog Pre-condition: Engine speed not zero */
#define IMO_NOT_UNLOCKED                         2U  /* Immobilizer not unlocked */
#define SERV_PRECOND_VEHICLE_SPEED               5U  /* Vehicle speed non-zero */
#define SUPPLY_VOLTAGE_TOO_LOW                  10U  /* KL30 is too low */
#define SECURE_STATE                            13U  /* Report that ECU is not in safety state for programming */
#define SPERRZEIT                              129U  /* Required time delay after failed security access not expired */
#define MAX_NUMBER_OF_PROGRAMMING_EXCEEDED     131U  /* Max programming session has been reached */
#define OVERVOLTAGE                            140U  /* Active discharge is in progress */
#define READINESS_CODE_NOT_RESETTED            141U  /* ODB DCY reached or 04 does not performed */
#define ONEPERSEC_TO_RPM_FACT                 60.0F    /* Convert 1/sec to rpm */
#define FAHRZYKL_INAKTIV                         0U
#define SERVICE_PRECOND_CYC_TIME                 20U      /* service precondition check cycle time [ms] */
#define SERVICE_PRECOND_SIGNAL_FILTER_TIME     2000U
#define SERVICE_PRECOND_CNT_TH               ((SERVICE_PRECOND_SIGNAL_FILTER_TIME/SERVICE_PRECOND_CYC_TIME)+1u)
#define NO_FALLBACK                  0U
#define NRC_RPM_TOO_HIGH             0x81U
#define NRC_VEH_SPEED_TOO_HIGH       0x88U
#define UDS_SERVICE_FALLBACK_NOT_REQ     0U
#define UDS_SERVICE_FALLBACK_REQ         1U
#define F1F1_ECURESET_NOT_REQ                    0U
#define F1F1_ECURESET_REQ                        1U
#define F1F1_ROUTINE_ID                          0xF1F1U
#define START_ROUTINE                            0x01U
#define ROUTINE_CONTROL_MIN_SIZE                 3U
#define BSWM_REQUESTING_USER_3                   3U
#define BSWM_REQUESTING_USER_1                   1U
#define PHYSICAL_ADDRESSING      0U
#define FUNCTIONAL_ADDRESSING    1U
#define CLEARRESETEMISSIONRELATEDDIAGNOSTICINFORMATION   0x04U
#define DIAGNOSTICSESSIONCONTROL                         0x10U
#define ECURESET                                         0x11U
#define READDATABYIDENTIFIER                             0x22U
#define COMMUNICATIONCONTROL                             0x28U
#define WRITEDATABYIDENTIFIER                            0x2EU
#define ROUTINECONTROL                                   0x31U
#define CONTROLDTCSETTING                                0x85U
#define REQEMISSINRELDTCSWITHPERMANENTSTATUS             0x0AU
#define UDS_CONFIRMED                                    0x00U
#define   PROG_CHECK_INGORE     0x00EB0000u
#define MAX_NUMOFDIDS_FUNCTIONALADDRESSING   6U
#define COMM_AND_NETWORK_TYPE                1U
#define NORMAL_COMMUNICATION_MESSGAES        1U
#define ROUTINE_CORRECT_RESULTS              0x20U
#define ROUTINE_INACTIVE                     0x0U
#define ROUTINE_ACTIVE                       0x1U
#define ROUTINE_ABORTED                      0x2U
#define ROUTINE_FINISHED_CORRECTLY           0x04U
#define NVM_INIT_PATTERN                                        0x494E4954
#define SAK_PENALTYTIME_SIZE                                            4u
#define SAK_BREAKINTRIES_SIZE                                           4u
#define BL_NUMBER_OF_ADMINTABLES                                        5u
#define BL_RAM_INIT_VALUE                                            0x2Du
#define GET_ERASE_CYCLES               (uint16)0U
#define DID_EE70_ENTRYCOUNT            (uint16)20U
#define DFLASH_SECTOR_RECOVERY_TIMEOUT (uint32)2000000000UL /* in x10 ns */
#define NVMSM_DFLASH_CLEARED           0x55U
#define NVMSM_DFLASH_HWFAILURE         0xAAU
#define NVMSM_DFLASH_INDICATOR         (uint8)1U
#define NVMSM_DFLASH_ERASE_COUNTER     (uint8)2U
#define DEM_ID_AURIX_HW_FLT_NVM_ERROR  DEM_EVENT_ID_INVALID
#define NVMSM_RDWAITTIMEOUT            500000000UL
#define NVMSM_WRWAITTIMEOUT            500000000UL
#define NVMSM_WRGCTIMEOUT              2000000000UL
#define NvM_SMs_START_SEC_BSW_CODE_LOCAL /* PRQA S 4800 */
#define NvM_SMs_STOP_SEC_BSW_CODE_LOCAL /* PRQA S 4800 */
#define OBD_CALLTIME 100U
#define OBD_DCY_INITIAL_VALUE    0U    /* Initial value befor the Obd_Init() function is called */
#define OBD_INIT                 1U    /* state: Init */
#define OBD_DELAY                2U    /* state: Delay */
#define OBD_WAIT                 3U    /* state: Wait */
#define OBD_QUALIF_DR            4U    /* state: Drive */
#define OBD_QUALIF_PR            5U    /* state: Post run (qualified) */
#define OBD_LATENT_PR            7U    /* state: Post run (latent) */
#define DCY_DELAY_TIME        2000U /* DCY_Delay [A: Q-LAH_80114-4137]*/
#define INFOTYPE_ECUNAME_SIZE    20U
#define CVN_CHECKSUM_SIZE         4U
#define PID_VEH_SPD_PHY_MAX_LIM        255.0F
#define NO_OBD                   0x05U  /* value according to J1979DA standard */
#define LEAST_LIKELY_PID_0D_VALUE   0xFFU
#define PMODE_FILTER_BYTE2       0x10U
#define PMODE_FUNC_OBD04         0x10U
#define PMODE_MAX_DISTTRAVELED   100.0F  /* [km] */
#define PMODE_ARRAY_SIZE               3U
#define OBD_VEHICLESPEED_DATA_LENGHT   1U
#define PID_42_SCALING     1000.0F
#define OBD_VEHICLE_ODOMETER_DATA_LENGHT  4U
#define CRC_INITIAL_VALUE32   (0xFFFFFFFFUL)
#define HOUR_TO_SEC                       3600.0F
#define TENTH_MULTIPLIER                  10.0F
#define VALIDITY_KMSTAND_FAILVALUE        0xFFFFFU
#define VALIDITY_KMSTAND_INITVALUE        0xFFFFEU
#define PMODE_DEACTIVATION_VALUE          0x00U
#define OBD_IGNCYCCNT_RESETVAL            0U
#define PI                     3.14159265F
#define PI_180                 0.017453293F
#define RSLVAGOFFS_FACT          0.01F
#define RSLVAGOFFS_OFFSET        ( -180.0F )
#define DIAG_VWAG_CAN            0U
#define DIAG_VWAG_CANFD          10U
#define DIAG_OBD_CANFD           20U
#define DIAG_OBDC_CANFD          30U
#define PROG_SIG_HIGH_FD         0x50726f68UL
#define PROG_SIG_LOW_FD          0x5369676fUL
#define PROG_SIG_HIGH            0x50726f67UL
#define PROG_SIG_LOW             0x5369676eUL
#define PROG_SIG_HIGH_OBDC_FD    0x50726f69UL
#define PROG_SIG_LOW_OBDC_FD     0x53696770UL
#define DEMEXT_PROTOCOL_OBD      DcmConf_DcmDslProtocol_OBDProtocol
#define DEMEXT_PROTOCOL_VW_AG    DcmConf_DcmDslProtocol_VWAGProtocol
#define DEMEXT_PROTOCOL_OBDC     DcmConf_DcmDslProtocol_OBDCProtocol
#define CAN_PROTOCOL             0x000000AAUL
#define CANFD_PROTOCOL           0x000000CCUL
#define OBDC_FD_PROTOCOL         0x000000DDUL
#define DEMEXT_CANIF_PDU_ISOX_EMOTOR_0X_RESP_FC      CanIfConf_CanIfTxPduCfg_ISOx_EMotor_01_Resp_FC_402522236T
#define DEMEXT_CANIF_PDU_ISOX_EMOTOR_0X_RESP_FD_FC   CanIfConf_CanIfTxPduCfg_ISOx_EMotor_01_Resp_FD_FC_474087548T
#define DEMEXT_CANIF_PDU_OBDC_EMOTOR_0X_RESP_FD_FC   CanIfConf_CanIfTxPduCfg_ipduOBDC_EMotor_01_Resp_FD_FC_474088060T
#define DEFAULT_SESSION_RESPONSE_ERASE_MASK              0xFFFFFDFFUL
#define PROTOCOL_MASK                                    0x000000FFUL
#define CBL_RESPONSE_REQUIRED                            0xFFU
#define CBL_RESPONSE_NOT_REQUIRED                        0xBBU
#define KEYOFFON_RESET                                   0x02U
#define HARD_RESET                                       0x01U
#define KEYOFFON_RESET_SUPP_POS_RESP                     0x82U
#define HARD_RESET_SUPP_POS_RESP                         0x81U
#define DID_0410_BOOTLOADERTPBLOCK_DEFAULT_VALUE         0x0FU
#define ADMINTABLE_VALID_RANGE                           0xFFFFFF00UL
#define SIXTYFOUR_BIT_OF_ONES_FOR_SBL_VALUE_CHECK        0xFFFFFFFFUL
#define MASKING_VALUE_FOR_SBL_ONES_ON_2_3_BYTE           0x0000FF00UL
#define MASKING_VALUE_FOR_SBL_ONES_ON_0_1_BYTE		      0x000000FFUL
#define ZERO_UL_FOR_LOGICAL_VALUE_CHECK			         0UL
#define ZERO_U_FOR_LOGICAL_VALUE_CHECK			            0U
#define ZERO_U_FOR_VALUE_ASSIGNMENT			               0U
#define VALUE_FOR_CALCULATION_OF_100ER_DIGIT_OF_SBL	   100U
#define VALUE_FOR_CALCULATION_OF_10ER_DIGIT_OF_SBL	      10UL
#define VALUE_FOR_CALCULATION_OF_1ER_DIGIT_OF_SBL        10UL
#define VALUE_FOR_ADDING_TO_SBL				               0x30U
#define SHIFTING_VALUE_FOR_SECUSRVVERSION                8U
#define SDULENGTH                   			            8U
#define POSITIVE_MSG_LENGTH_RES_DATALEN                  1U
#define POSITIVE_MSG_DATA                                2U
#define RESOLVER_CALIBRATION_NEVER_EXECUTED              0U
#define RESOLVER_CALIBRATION_FAILED                      1U
#define RESOLVER_CALIBRATION_SUCCESSFUL                  2U
#define RESOLVER_CALIBRATION_CRC_ERROR                   3U
#define NO_VALID_VALUE_FOR_RETURN                        0x00U
#define WARM_RESET_DUE_TO_SERIES_SWITCH_OVER		         1U
#define ROM_END_VALUE					                     0x003FFFFFUL
#define START_OF_CACHABLE_ADDRESS		                  0x80000000UL
#define START_OF_NON_CACHABLE_ADDRESS			            0xA0000000UL
#define MASK_FOR_REMOVING_THE_HIGHEST_BYTE		         0x0FFFFFFFUL
#define DISABLE_CAN_COMMUNICATION			               1U
#define SID_SESSION_CONTROL_LENGTH_OF_PAYLOAD            0x06U
#define SID_SESSION_CONTROL_POS_RESP                     0x50U
#define SID_SESSION_CONTROL_SUBFUNCTION                  0x01U
#define SID_SESSION_CONTROL_PROTOCOL_TIMING_0            0x00U
#define SID_SESSION_CONTROL_PROTOCOL_TIMING_1            0x19U
#define SID_SESSION_CONTROL_PROTOCOL_TIMING_2            0x01U
#define SID_SESSION_CONTROL_PROTOCOL_TIMING_3            0xE5U
#define SID_HARD_RESET_LENGTH_OF_PAYLOAD                 0x02U
#define SID_HARD_RESET_POS_RESP                          0x51U
#define SID_HARD_RESET_SUBFUNCTION                       0x01U
#define UTIL_SWAP_MAX_SIZE   4U
#define MOVE_FORWARD    1L
#define MOVE_BACKWARD  -1L
#define TDP_DIDBUF_INIT_EVENT          (0xFFFFU)
#define BSWERRDEB_DEM_EVENT_ERRDEB_INACTIVE_STATUS   0x7FU
#define BM_ADMIN_BLOCK_ADDRESS            0x80000020U
#define SBL_VERSION_ADDRESS               0x8033E100U
#define SBL_OEM_VW_VERSION                0x00000500U  /* VW = 05 xx */
#define FW_BM_NUMBER_OF_VERSION_BYTES     4U
#define FW_SBL_NUMBER_OF_VERSION_BYTES    4U
#define FW_HSM_NUMBER_OF_VERSION_BYTES    4U
#define FW_PU_BM_NUMBER_OF_VERSION_BYTES  4U
#define FW_PU_BL_NUMBER_OF_VERSION_BYTES  4U
#define VD                                0xFFu
#define IV                                0x00u
#define VCC_BOOT_SW_RUNNING_RESET         0xA55AAAAAUL
#define ASCII_CHARACTER_CAPITAL_R         0x52U /* hex value for char 'R' */
#define ASCII_CHARACTER_CAPITAL_F         0x46U /* hex value for char 'F' */
#define ASCII_CHARACTER_CAPITAL_S         0x53U /* hex value for char 'S' */
#define ASCII_CHARACTER_CAPITAL_V         0x56U /* hex value for char 'V' */
#define ASCII_NUMBER_ONE                  0x31U /* hex value for char '1' */
#define ASCII_DOT                         0x2EU /* hex value for char '.' */
#define ASCII_NUMBER_ZERO                 0x30U /* hex value for char '0' */
#define RfsV_SIZE                         4u /* PRQA S 4800 */
#define PTL_I_SIZE                        7u         /* [A: 80126-A1281] */
#define PTL_I_ID  {ASCII_CHARACTER_CAPITAL_R, ASCII_CHARACTER_CAPITAL_F, ASCII_CHARACTER_CAPITAL_S, ASCII_CHARACTER_CAPITAL_V, \
#define DGP_NUMBER_OF_BLOCKS              4u                   /* Logical blocks :BLU +APP +Data +M0 */
#define  PROG_SEG_BLU 0x1
#define  PROG_SEG_APP 0x2
#define  PROG_SEG_DATA 0x3
#define  PROG_SEG_M0 0x4
#define RSRVD8  (0xFFU)
#define RSRVD16 (0xFFFFU)
#define RSRVD32 (0xFFFFFFFFUL)
#define SFTY_C2C_AES128_DATA_LEN  (16U)
#define ASCII_a 97U
#define ASCII_b 98U
#define ASCII_c 99U
#define ASCII_d 100U
#define ASCII_e 101U
#define ASCII_f 102U
#define ASCII_g 103U
#define ASCII_h 104U
#define ASCII_i 105U
#define ASCII_j 106U
#define ASCII_k 107U
#define ASCII_l 108U
#define ASCII_m 109U
#define ASCII_n 110U
#define ASCII_o 111U
#define ASCII_p 112U
#define ASCII_q 113U
#define ASCII_r 114U
#define ASCII_s 115U
#define ASCII_t 116U
#define ASCII_u 117U
#define ASCII_v 118U
#define ASCII_w 119U
#define ASCII_x 120U
#define ASCII_y 121U
#define ASCII_z 122U
#define ASCII_A 65U
#define ASCII_B 66U
#define ASCII_C 67U
#define ASCII_D 68U
#define ASCII_E 69U
#define ASCII_F 70U
#define ASCII_G 71U
#define ASCII_H 72U
#define ASCII_I 73U
#define ASCII_J 74U
#define ASCII_K 75U
#define ASCII_L 76U
#define ASCII_M 77U
#define ASCII_N 78U
#define ASCII_O 79U
#define ASCII_P 80U
#define ASCII_Q 81U
#define ASCII_R 82U
#define ASCII_S 83U
#define ASCII_T 84U
#define ASCII_U 85U
#define ASCII_V 86U
#define ASCII_W 87U
#define ASCII_X 88U
#define ASCII_Y 89U
#define ASCII_Z 90U
#define ASCII_0 48U
#define ASCII_1 49U
#define ASCII_2 50U
#define ASCII_3 51U
#define ASCII_4 52U
#define ASCII_5 53U
#define ASCII_6 54U
#define ASCII_7 55U
#define ASCII_8 56U
#define ASCII_9 57U
#define ASCII_NULL 0U
#define ASCII_SPA 32U /*   */
#define ASCII_MUL 42U /* * */
#define ASCII_PLU 43U /* + */
#define ASCII_MIN 45U /* - */
#define ASCII_DIV 47U /* / */
#define ASCII_UND 95U /* _ */
#define SWIT_FLOAT32 0
#define SWIT_UINT8 1
#define SWIT_UINT16 2
#define SWIT_UINT32 3
#define SWIT_FLOAT32_A 5
#define SWIT_FLOAT32_P 6
#define SWIT_SINT16  (7)
#define SWIT_SINT32   11
#define SWIT_SINT16_Sin 8
#define SWIT_UINT16_Sin 9
#define SWIT_UINT16_Sin_N 10
#define SWIT_2FLOAT32 16
#define SWIT_3FLOAT32 17
#define SWIT_UINT32_P 19
#define SWIT_UINT16_P 21
#define SWIT_UINT8_N 22
#define SWIT_UINT8_P 23
#define SWIT_FLOAT32_N 24
#define SWIT_SINT32_P 25
#define SWIT_SINT32_N 26
#define SWIT_SFTY_INTERFACES_MAIN_KEY_ENABLE 1
#define TqMgr_EN_KEY 7900
#define IvtrHvDcI2tDrtg_EN_KEY 8000
#define SWIT_DRCO_INTERFACES_MAIN_KEY_ENABLE 1
#define SWIT_ReqIAcExtLim_Output_KEY 3004
#define SWIT_ReqIAcMaxLim1_Output_KEY 3005
#define SWIT_ReqIAcMaxLim2_Output_KEY 3006
#define SWIT_DrvCtrlC2cData_IgbtLosses_Output_KEY 10201
#define SWIT_DrvCtrlC2cData_ElLossesFlt_Output_KEY 10202
#define SWIT_DrvCtrlC2cData_PwrElecAct_Output_KEY 10203
#define SWIT_DrvCtrlC2cData_TqAct_Output_KEY 10204
#define SWIT_DrvCtrlC2cData_EmAndIvtrPwrLossHvDcPwrLimMot_Output_KEY 10205
#define SWIT_DrvCtrlC2cData_EmAndIvtrPwrLossHvDcPwrLimGen_Output_KEY 10206
#define SWIT_DrvCtrlC2cData_EmAndIvtrPwrLossHvDcPwrTotLimMot_Output_KEY 10207
#define SWIT_DrvCtrlC2cData_EmAndIvtrPwrLossHvDcPwrTotLimGen_Output_KEY 10208
#define SWIT_SftyC2cData_CpldFltCtrlOvrdReq_Output_KEY 10209
#define SWIT_BswC2cData_CpldFltCtrlOvrdSts_Output_KEY 9101
#define SWIT_tqSpSelLoc_Input_KEY 9801
#define SWIT_ALVCNTRCORE2_KEY 7606
#define SWIT_TRAPCORE2_KEY 7607
#define SWIT_SMUALRMCORE2_KEY 7608
#define SWIT_HvAcPwrCalcnAcPwr_Output_KEY          3000
#define SWIT_IvtrThermMdlPwrLossIvtr_Output_KEY    3001
#define SWIT_DrvCtrlSeqrStsInvSafeSt_Output_KEY    3003
#define SWIT_RslvrCalcnTiStamp_Output_KEY        4000
#define SWIT_RslvrCalcnTiStamp_Input_KEY         4001
#define SWIT_RslvrCalcnAgMeclRslvr_Output_KEY    4002
#define SWIT_RslvrCalcnAgMeclRslvr_Input_KEY     4003
#define SWIT_RslvrCalcnSpdMeclRslvr_Input_KEY    4004
#define SWIT_EncCalcnExtrpnAgMecl_Output_KEY     4005
#define SWIT_EncCalcnAgMecl_Output_KEY           4006
#define SWIT_EncCalcnSpdMecl_Input_KEY           4008
#define SWIT_EncCalcnAgMecl_Input_KEY            4009
#define SWIT_EncFilAgMecl_Output_KEY             4010
#define SWIT_EncFilAgMecl_Input_KEY              4011
#define SWIT_RotorAgSpdCalcnAgMeclF_Output_KEY   4012
#define SWIT_RotorAgSpdCalcnSpdMeclFild0_Input_KEY 4007
#define SWIT_DrvCtrlC2cData_SpdActRpm_Input_KEY  4013
#define SWIT_HvDcICalcnIDc_Output_KEY            4014
#define SWIT_HvAcICalcnLocIMeasIPhaOld_OUTPUT_KEY 5000
#define SWIT_HvAcICalcnLocIPha_OUTPUT_KEY 5001
#define SWIT_HvAcICalcnLocIPha_OUTPUT_KEY1 5002
#define SWIT_PhaFailSngRun_InputData_OUTPUT_KEY 5003
#define SWIT_DrvCtrlC2cData_CooltRateFlowEstimd_Output_KEY 7801
#define SWIT_DrvCtrlC2cData_PmTempCalcnSt_KEY 7806
#define SWIT_CpuLoad_Output_KEY 7810
#define SWIT_ResolverOffset_Output_KEY 7811
#define SWIT_ResolverOffsetSin_Output_KEY 7812
#define SWIT_ResolverOffsetCos_Output_KEY 7813
#define SWIT_RstHndlr_Output_KEY 7814
#define SWIT_P14HvLvU_Output_KEY 7815
#define SWIT_RslvrCosAmp_Output_KEY 7816
#define SWIT_RslvrSinAmp_Output_KEY 7817
#define SWIT_RslvrExctAmp_Output_KEY 7818
#define SWIT_P15CurU_Output_KEY 7819
#define SWIT_Kl30U_Output_KEY 7820
#define SWIT_Rsh_OruState_Input_KEY 7821
#define SWIT_PMode_MaxDistReached_Input_KEY 7822
#define SWIT_PMode_Config0_Input_KEY 7823
#define SWIT_PMode_Config1_Input_KEY 7824
#define SWIT_PMode_SigSts_Input_KEY 7825
#define SWIT_VAG_BL_Output_KEY 7826
#define SWIT_Idp_x0407_blockData1_KEY1 7827
#define SWIT_Idp_x0407_blockData1_KEY2 7828
#define SWIT_Idp_x0407_blockData1_KEY3 7829
#define SWIT_Xcp_ControlStateOfXcpModule_Input_KEY 7401
#define SWIT_SCU_OVCCON_Input_KEY 7402
#define SWIT_Rsh_CheckProgrammingConditions_Start_Output_KEY 7403
#define SWIT_Dcm_GetProgConditions_Output_KEY 7404
#define SWIT_Dcm_SetProgConditions_Start_Output_KEY 7405
#define SWIT_BswC2cData_InvEmTempNvm_NvmTempVld_Output_KEY 8100
#define SWIT_IvtrIgbtTempEvln_IgbtTempPhaU_Output_KEY 8401
#define SWIT_IvtrIgbtTempEvln_IgbtTempPhaV_Output_KEY 8402
#define SWIT_CanBatteryMode_HvDcUCtrl_Input_KEY 425
#define SWIT_CanBatteryMode_SpoMaxEmSpdCalcn_Input_KEY 426
#define SWIT_HvDcUCalcnUDc_HvDcULimn_INPUT_KEY 8000
#define SWIT_HvDcUCalcnUDc_IpmCtrl_INPUT_KEY 8001
#define SWIT_HvDcUCalcnUDc_ModlnIdxCalcn_INPUT_KEY 8003
#define SWIT_HvDcUCalcnUDcFild0_SpoMaxEmSpdCalcn_INPUT_KEY 8010
#define SWIT_HvDcUCalcnUDcFild0_IpmCtrl_INPUT_KEY 8011
#define SWIT_HvDcUCalcnUDcFild0_HvDcUCtrl_INPUT_KEY 8012
#define SWIT_HvDcUCalcnUDcFild1_RslvrOffsDetn_INPUT_KEY 8020
#define SWIT_HvDcUCalcnUDcFild1_TqMgr_INPUT_KEY 8021
#define SWIT_TqCtrlAcPwrElec_Output_KEY 9601
#define SWIT_IvtrThermMdlIvtrTotPwrLoss_Output_KEY 9602
#define SWIT_HvDcUCalcnUDcFild0_Output_KEY 9603
#define SWIT_DrvCtrlSeqrPlsEnaSts_Output_KEY 9604
#define SWIT_IvtrThermMdlIgbtJcnTempCooltTempDelta_Output_KEY 9701
#define SWIT_IvtrThermMdlJcnTempMax_Output_KEY 9702
#define SWIT_HvDcULimnTqLimMin_Output_KEY 10008
#define SWIT_HvDcULimnTqLimMax_Output_KEY 10009
#define SWIT_TqCtrlTqAvlMin_Output_KEY    10010
#define SWIT_TqCtrlTqAvlMax_Output_KEY    10011
#define SWIT_TqMgrTqDrtgMax_Output_KEY    10013
#define SWIT_TqMgrTqLimMax_Output_KEY     10014
#define SWIT_TqMgrTqLimMin_Output_KEY     10015
#define SWIT_TqMgrExtdTqLimTqMax_Output_KEY 10016
#define SWIT_TqMgrI2tDcLinkTqMin_Output_KEY 10019
#define SWIT_TqShaftAvlMaxMin0_Output_KEY 10022
#define SWIT_TqShaftAvlMaxMin1_Output_KEY 10023
#define SWIT_TqMgrDrtgTqLimMin_Output_KEY 10501
#define SWIT_TqMgrDrtgTqLimMax_Output_KEY 10502
#define SWIT_TqMgrTotTqLimMin_Output_KEY 10503
#define SWIT_TqMgrTotTqLimMax_Output_KEY 10504
#define SWIT_EmAndIvtrPwrLossHvDcLoadPwrGen_Output_KEY  10505
#define SWIT_IgbtLosses_Output_KEY 10506
#define SWIT_ElLossesFlt_Output_KEY 10507
#define SWIT_IDcActFild_Output_KEY  10508
#define SWIT_TqMgrExtdTqLimMax_Output_KEY 10509
#define SWIT_TqMgrExtdTqLimMin_Output_KEY 10510
#define SWIT_TqCtrlEmAndCablePwrLoss_Output_KEY 10022
#define SWIT_TqCtrlEmAndCablePwrLossMax_Output_KEY 10023
#define SWIT_IvtrThermMdlIvtrPwrLossMax_Output_KEY 10024
#define SWIT_SI_P_Mode_gueltig_Output_KEY 10025
#define SWIT_SI_P_Mode_Output_KEY 10026
#define SWIT_KBI_Kilometerstand_Output_KEY 10027
#define SWIT_TqPrednGenMomTqLimGen_Output_KEY 7804
#define SWIT_DrvCtrlC2cData_IvtrCooltInlTemp_Output_KEY 7805
#define SWIT_IvtrDcLinkThermMdl_OutputData_BbTemp_Output_KEY 4015
#define SWIT_IvtrDcLinkThermMdl_OutputData_CpTemp_Output_KEY 4016
#define SWIT_DrvCtrlSeqrStInt_Output_KEY								(4021)
#define SWIT_SftyC2cData_StabPwrSply_Input_KEY							(3375)
#define SWIT_SftyC2cData_ActvDchaReq_Input_KEY                          (1687)
#define SWIT_SftyC2cData_HwpFltCtrlOvrdReq_Input_KEY					(4053)
#define SWIT_SftyC2cData_P2V5CuCmpFac_Input_KEY							(4011)
#define SWIT_SftyC2cData_StsInvSafeSt_Input_KEY                         (1963)
#define SWIT_SftyC2cData_OperRdy_Input_KEY                              (3373)
#define SWIT_HvDcUMeasUDcFild2_Output_KEY                               (4017)
#define SWIT_HvDcUMeasUDcFild2_Input_KEY                                (4018)
#define SWIT_HvDcUMeasUDcFild1_Output_KEY                               (4019)
#define SWIT_RotorAgSpdCalcnAgVld_Input_KEY                             (4019)
#define SWIT_HvDcUMeasUDc_Output_KEY                                    (4020)
#define SWIT_SftyC2cData_RslvrOffs_Input_KEY                            (1633)
#define SWIT_HvDcUMeasUDcFild1_Input_KEY                                (4050)
#define SWIT_DrvCtrlC2cData_UDcActFild1_Output_KEY                      (10524)
#define SWIT_DrvCtrlC2cData_UDcActFild1_Input_KEY                       (10525)
#define SWIT_DrvCtrlC2cData_UDcActFild10_Output_KEY                     (10526)
#define SWIT_DrvCtrlC2cData_UDcActFild10_Input_KEY                      (10527)
#define SWIT_CpuLoad_Input_KEY                                          (10528)
#define SWIT_DrvCtrlSeqrIqReq_Output_KEY                                (4081)
#define SWIT_DrvCtrlSeqrIdReq_Output_KEY                                (4082)
#define SWIT_DrvCtrlSeqrIdIqSlewRate_Input_KEY                          (4083)
#define SWIT_DrvCtrlSeqrIdIqReqEna_Input_KEY                            (4084)
#define SWIT_DrvCtrlSeqrIqReq_Input_KEY                                 (4085)
#define SWIT_DrvCtrlSeqrIdReq_Input_KEY                                 (4086)
#define SWIT_EncFilSpdMecl_Output_KEY                                   (4087)
#define SWIT_RotorAgSpdCalcnSpdMeclFild2_Input_KEY                      (4088)
#define SWIT_HvDcUMeasUDcFild10_KEY                                     (4089)
#define SWIT_DRCO_Stack_KEY     (200)


int main () {
	#ifdef SWIT_Active
		printf("0\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("1\n");
	#else
		printf("2\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("3\n");
	#else
		printf("4\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("5\n");
	#else
		printf("6\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("7\n");
	#else
		printf("8\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("9\n");
	#else
		printf("10\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("11\n");
	#else
		printf("12\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("13\n");
	#else
		printf("14\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("15\n");
	#else
		printf("16\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("17\n");
	#else
		printf("18\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("19\n");
	#else
		printf("20\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("21\n");
	#else
		printf("22\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("23\n");
	#else
		printf("24\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("25\n");
	#else
		printf("26\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("27\n");
	#else
		printf("28\n");
	#endif
	#ifdef SWIT_Active
		printf("29\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("30\n");
	#else
		printf("31\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("32\n");
	#else
		printf("33\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("34\n");
	#else
		printf("35\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("36\n");
	#else
		printf("37\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("38\n");
	#else
		printf("39\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("40\n");
	#else
		printf("41\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("42\n");
	#else
		printf("43\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("44\n");
	#else
		printf("45\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("46\n");
	#else
		printf("47\n");
	#endif
	#ifdef RTE_PTR2ARRAYTYPE_PASSING
		printf("48\n");
	#else
		printf("49\n");
	#endif
	#ifdef SWIT_Active
		printf("50\n");
	#endif
	#ifdef SWIT_Active
		printf("51\n");
	#endif
	#ifdef SWIT_Active
		printf("52\n");
	#endif
	return 0;
}