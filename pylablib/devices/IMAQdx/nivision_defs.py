##########   This file is generated automatically based on nivision.h   ##########

# pylint: disable=unused-import, unused-argument, wrong-spelling-in-comment


import ctypes
import enum
from ...core.utils import ctypes_wrap




def _int32(v): return (v+0x80000000)%0x100000000-0x80000000




##### DEFINE GROUPS #####


class ERR(enum.IntEnum):
    ERR_SUCCESS                                              = _int32(0)
    ERR_SYSTEM_ERROR                                         = _int32(-1074396160)
    ERR_OUT_OF_MEMORY                                        = _int32(-1074396159)
    ERR_MEMORY_ERROR                                         = _int32(-1074396158)
    ERR_UNREGISTERED                                         = _int32(-1074396157)
    ERR_NEED_FULL_VERSION                                    = _int32(-1074396156)
    ERR_UNINIT                                               = _int32(-1074396155)
    ERR_IMAGE_TOO_SMALL                                      = _int32(-1074396154)
    ERR_BARCODE_CODABAR                                      = _int32(-1074396153)
    ERR_BARCODE_CODE39                                       = _int32(-1074396152)
    ERR_BARCODE_CODE93                                       = _int32(-1074396151)
    ERR_BARCODE_CODE128                                      = _int32(-1074396150)
    ERR_BARCODE_EAN8                                         = _int32(-1074396149)
    ERR_BARCODE_EAN13                                        = _int32(-1074396148)
    ERR_BARCODE_I25                                          = _int32(-1074396147)
    ERR_BARCODE_MSI                                          = _int32(-1074396146)
    ERR_BARCODE_UPCA                                         = _int32(-1074396145)
    ERR_BARCODE_CODE93_SHIFT                                 = _int32(-1074396144)
    ERR_BARCODE_TYPE                                         = _int32(-1074396143)
    ERR_BARCODE_INVALID                                      = _int32(-1074396142)
    ERR_BARCODE_CODE128_FNC                                  = _int32(-1074396141)
    ERR_BARCODE_CODE128_SET                                  = _int32(-1074396140)
    ERR_ROLLBACK_RESOURCE_OUT_OF_MEMORY                      = _int32(-1074396139)
    ERR_ROLLBACK_NOT_SUPPORTED                               = _int32(-1074396138)
    ERR_DIRECTX_DLL_NOT_FOUND                                = _int32(-1074396137)
    ERR_DIRECTX_INVALID_FILTER_QUALITY                       = _int32(-1074396136)
    ERR_INVALID_BUTTON_LABEL                                 = _int32(-1074396135)
    ERR_THREAD_INITIALIZING                                  = _int32(-1074396134)
    ERR_THREAD_COULD_NOT_INITIALIZE                          = _int32(-1074396133)
    ERR_MASK_NOT_TEMPLATE_SIZE                               = _int32(-1074396132)
    ERR_NOT_RECT_OR_ROTATED_RECT                             = _int32(-1074396130)
    ERR_ROLLBACK_UNBOUNDED_INTERFACE                         = _int32(-1074396129)
    ERR_ROLLBACK_RESOURCE_CONFLICT_3                         = _int32(-1074396128)
    ERR_ROLLBACK_RESOURCE_CONFLICT_2                         = _int32(-1074396127)
    ERR_ROLLBACK_RESOURCE_CONFLICT_1                         = _int32(-1074396126)
    ERR_INVALID_CONTRAST_THRESHOLD                           = _int32(-1074396125)
    ERR_INVALID_CALIBRATION_ROI_MODE                         = _int32(-1074396124)
    ERR_INVALID_CALIBRATION_MODE                             = _int32(-1074396123)
    ERR_DRAWTEXT_COLOR_MUST_BE_GRAYSCALE                     = _int32(-1074396122)
    ERR_SATURATION_THRESHOLD_OUT_OF_RANGE                    = _int32(-1074396121)
    ERR_NOT_IMAGE                                            = _int32(-1074396120)
    ERR_CUSTOMDATA_INVALID_KEY                               = _int32(-1074396119)
    ERR_INVALID_STEP_SIZE                                    = _int32(-1074396118)
    ERR_MATRIX_SIZE                                          = _int32(-1074396117)
    ERR_CALIBRATION_INSF_POINTS                              = _int32(-1074396116)
    ERR_CALIBRATION_IMAGE_CORRECTED                          = _int32(-1074396115)
    ERR_CALIBRATION_INVALID_ROI                              = _int32(-1074396114)
    ERR_CALIBRATION_IMAGE_UNCALIBRATED                       = _int32(-1074396113)
    ERR_INCOMP_MATRIX_SIZE                                   = _int32(-1074396112)
    ERR_CALIBRATION_FAILED_TO_FIND_GRID                      = _int32(-1074396111)
    ERR_CALIBRATION_INFO_VERSION                             = _int32(-1074396110)
    ERR_CALIBRATION_INVALID_SCALING_FACTOR                   = _int32(-1074396109)
    ERR_CALIBRATION_ERRORMAP                                 = _int32(-1074396108)
    ERR_CALIBRATION_INFO_1                                   = _int32(-1074396107)
    ERR_CALIBRATION_INFO_2                                   = _int32(-1074396106)
    ERR_CALIBRATION_INFO_3                                   = _int32(-1074396105)
    ERR_CALIBRATION_INFO_4                                   = _int32(-1074396104)
    ERR_CALIBRATION_INFO_5                                   = _int32(-1074396103)
    ERR_CALIBRATION_INFO_6                                   = _int32(-1074396102)
    ERR_CALIBRATION_INFO_MICRO_PLANE                         = _int32(-1074396101)
    ERR_CALIBRATION_INFO_PERSPECTIVE_PROJECTION              = _int32(-1074396100)
    ERR_CALIBRATION_INFO_SIMPLE_TRANSFORM                    = _int32(-1074396099)
    ERR_RESERVED_MUST_BE_NULL                                = _int32(-1074396098)
    ERR_INVALID_PARTICLE_PARAMETER_VALUE                     = _int32(-1074396097)
    ERR_NOT_AN_OBJECT                                        = _int32(-1074396096)
    ERR_CALIBRATION_DUPLICATE_REFERENCE_POINT                = _int32(-1074396095)
    ERR_ROLLBACK_RESOURCE_CANNOT_UNLOCK                      = _int32(-1074396094)
    ERR_ROLLBACK_RESOURCE_LOCKED                             = _int32(-1074396093)
    ERR_ROLLBACK_RESOURCE_NON_EMPTY_INITIALIZE               = _int32(-1074396092)
    ERR_ROLLBACK_RESOURCE_UNINITIALIZED_ENABLE               = _int32(-1074396091)
    ERR_ROLLBACK_RESOURCE_ENABLED                            = _int32(-1074396090)
    ERR_ROLLBACK_RESOURCE_REINITIALIZE                       = _int32(-1074396089)
    ERR_ROLLBACK_RESIZE                                      = _int32(-1074396088)
    ERR_ROLLBACK_STOP_TIMER                                  = _int32(-1074396087)
    ERR_ROLLBACK_START_TIMER                                 = _int32(-1074396086)
    ERR_ROLLBACK_INIT_TIMER                                  = _int32(-1074396085)
    ERR_ROLLBACK_DELETE_TIMER                                = _int32(-1074396084)
    ERR_ROLLBACK_TIMEOUT                                     = _int32(-1074396083)
    ERR_PALETTE_NOT_SUPPORTED                                = _int32(-1074396082)
    ERR_BAD_PASSWORD                                         = _int32(-1074396081)
    ERR_INVALID_IMAGE_TYPE                                   = _int32(-1074396080)
    ERR_INVALID_METAFILE_HANDLE                              = _int32(-1074396079)
    ERR_INCOMP_TYPE                                          = _int32(-1074396077)
    ERR_COORD_SYS_FIRST_AXIS                                 = _int32(-1074396076)
    ERR_COORD_SYS_SECOND_AXIS                                = _int32(-1074396075)
    ERR_INCOMP_SIZE                                          = _int32(-1074396074)
    ERR_MASK_OUTSIDE_IMAGE                                   = _int32(-1074396073)
    ERR_INVALID_BORDER                                       = _int32(-1074396072)
    ERR_INVALID_SCAN_DIRECTION                               = _int32(-1074396071)
    ERR_INVALID_FUNCTION                                     = _int32(-1074396070)
    ERR_INVALID_COLOR_MODE                                   = _int32(-1074396069)
    ERR_INVALID_ACTION                                       = _int32(-1074396068)
    ERR_IMAGES_NOT_DIFF                                      = _int32(-1074396067)
    ERR_INVALID_POINTSYMBOL                                  = _int32(-1074396066)
    ERR_CANT_RESIZE_EXTERNAL                                 = _int32(-1074396065)
    ERR_EXTERNAL_NOT_SUPPORTED                               = _int32(-1074396064)
    ERR_EXTERNAL_ALIGNMENT                                   = _int32(-1074396063)
    ERR_INVALID_TOLERANCE                                    = _int32(-1074396062)
    ERR_INVALID_WINDOW_SIZE                                  = _int32(-1074396061)
    ERR_JPEG2000_LOSSLESS_WITH_FLOATING_POINT                = _int32(-1074396060)
    ERR_INVALID_MAX_ITERATIONS                               = _int32(-1074396059)
    ERR_INVALID_ROTATION_MODE                                = _int32(-1074396058)
    ERR_INVALID_SEARCH_VECTOR_WIDTH                          = _int32(-1074396057)
    ERR_INVALID_MATRIX_MIRROR_MODE                           = _int32(-1074396056)
    ERR_INVALID_ASPECT_RATIO                                 = _int32(-1074396055)
    ERR_INVALID_CELL_FILL_TYPE                               = _int32(-1074396054)
    ERR_INVALID_BORDER_INTEGRITY                             = _int32(-1074396053)
    ERR_INVALID_DEMODULATION_MODE                            = _int32(-1074396052)
    ERR_INVALID_CELL_FILTER_MODE                             = _int32(-1074396051)
    ERR_INVALID_ECC_TYPE                                     = _int32(-1074396050)
    ERR_INVALID_MATRIX_POLARITY                              = _int32(-1074396049)
    ERR_INVALID_CELL_SAMPLE_SIZE                             = _int32(-1074396048)
    ERR_INVALID_LINEAR_AVERAGE_MODE                          = _int32(-1074396047)
    ERR_INVALID_2D_BARCODE_CONTRAST_FOR_ROI                  = _int32(-1074396046)
    ERR_INVALID_2D_BARCODE_SUBTYPE                           = _int32(-1074396045)
    ERR_INVALID_2D_BARCODE_SHAPE                             = _int32(-1074396044)
    ERR_INVALID_2D_BARCODE_CELL_SHAPE                        = _int32(-1074396043)
    ERR_INVALID_2D_BARCODE_CONTRAST                          = _int32(-1074396042)
    ERR_INVALID_2D_BARCODE_TYPE                              = _int32(-1074396041)
    ERR_DRIVER                                               = _int32(-1074396040)
    ERR_IO_ERROR                                             = _int32(-1074396039)
    ERR_FIND_COORDSYS_MORE_THAN_ONE_EDGE                     = _int32(-1074396038)
    ERR_TIMEOUT                                              = _int32(-1074396037)
    ERR_INVALID_SKELETONMODE                                 = _int32(-1074396036)
    ERR_TEMPLATEIMAGE_NOCIRCLE                               = _int32(-1074396035)
    ERR_TEMPLATEIMAGE_EDGEINFO                               = _int32(-1074396034)
    ERR_TEMPLATEDESCRIPTOR_LEARNSETUPDATA                    = _int32(-1074396033)
    ERR_TEMPLATEDESCRIPTOR_ROTATION_SEARCHSTRATEGY           = _int32(-1074396032)
    ERR_INVALID_TETRAGON                                     = _int32(-1074396031)
    ERR_TOO_MANY_CLASSIFICATION_SESSIONS                     = _int32(-1074396030)
    ERR_TIME_BOUNDED_EXECUTION_NOT_SUPPORTED                 = _int32(-1074396028)
    ERR_INVALID_COLOR_RESOLUTION                             = _int32(-1074396027)
    ERR_INVALID_PROCESS_TYPE_FOR_EDGE_DETECTION              = _int32(-1074396026)
    ERR_INVALID_ANGLE_RANGE_FOR_STRAIGHT_EDGE                = _int32(-1074396025)
    ERR_INVALID_MIN_COVERAGE_FOR_STRAIGHT_EDGE               = _int32(-1074396024)
    ERR_INVALID_ANGLE_TOL_FOR_STRAIGHT_EDGE                  = _int32(-1074396023)
    ERR_INVALID_SEARCH_MODE_FOR_STRAIGHT_EDGE                = _int32(-1074396022)
    ERR_INVALID_KERNEL_SIZE_FOR_EDGE_DETECTION               = _int32(-1074396021)
    ERR_INVALID_GRADING_MODE                                 = _int32(-1074396020)
    ERR_INVALID_THRESHOLD_PERCENTAGE                         = _int32(-1074396019)
    ERR_INVALID_EDGE_POLARITY_SEARCH_MODE                    = _int32(-1074396018)
    ERR_OPENING_NEWER_AIM_GRADING_DATA                       = _int32(-1074396017)
    ERR_NO_VIDEO_DRIVER                                      = _int32(-1074396016)
    ERR_RPC_EXECUTE_IVB                                      = _int32(-1074396015)
    ERR_INVALID_VIDEO_BLIT                                   = _int32(-1074396014)
    ERR_ZERO_BIT_DEPTH_FOR_16BIT_SGL_IMAGE                   = _int32(-1074395452)
    ERR_INVALID_VIDEO_MODE                                   = _int32(-1074396013)
    ERR_RPC_EXECUTE                                          = _int32(-1074396012)
    ERR_RPC_BIND                                             = _int32(-1074396011)
    ERR_INVALID_FRAME_NUMBER                                 = _int32(-1074396010)
    ERR_DIRECTX                                              = _int32(-1074396009)
    ERR_DIRECTX_NO_FILTER                                    = _int32(-1074396008)
    ERR_DIRECTX_INCOMPATIBLE_COMPRESSION_FILTER              = _int32(-1074396007)
    ERR_DIRECTX_UNKNOWN_COMPRESSION_FILTER                   = _int32(-1074396006)
    ERR_INVALID_AVI_SESSION                                  = _int32(-1074396005)
    ERR_DIRECTX_CERTIFICATION_FAILURE                        = _int32(-1074396004)
    ERR_AVI_DATA_EXCEEDS_BUFFER_SIZE                         = _int32(-1074396003)
    ERR_INVALID_LINEGAUGEMETHOD                              = _int32(-1074396002)
    ERR_TOO_MANY_AVI_SESSIONS                                = _int32(-1074396001)
    ERR_FILE_FILE_HEADER                                     = _int32(-1074396000)
    ERR_FILE_FILE_TYPE                                       = _int32(-1074395999)
    ERR_FILE_COLOR_TABLE                                     = _int32(-1074395998)
    ERR_FILE_ARGERR                                          = _int32(-1074395997)
    ERR_FILE_OPEN                                            = _int32(-1074395996)
    ERR_FILE_NOT_FOUND                                       = _int32(-1074395995)
    ERR_FILE_TOO_MANY_OPEN                                   = _int32(-1074395994)
    ERR_FILE_IO_ERR                                          = _int32(-1074395993)
    ERR_FILE_PERMISSION                                      = _int32(-1074395992)
    ERR_FILE_INVALID_TYPE                                    = _int32(-1074395991)
    ERR_FILE_GET_INFO                                        = _int32(-1074395990)
    ERR_FILE_READ                                            = _int32(-1074395989)
    ERR_FILE_WRITE                                           = _int32(-1074395988)
    ERR_FILE_EOF                                             = _int32(-1074395987)
    ERR_FILE_FORMAT                                          = _int32(-1074395986)
    ERR_FILE_OPERATION                                       = _int32(-1074395985)
    ERR_FILE_INVALID_DATA_TYPE                               = _int32(-1074395984)
    ERR_FILE_NO_SPACE                                        = _int32(-1074395983)
    ERR_INVALID_FRAMES_PER_SECOND                            = _int32(-1074395982)
    ERR_INSUFFICIENT_BUFFER_SIZE                             = _int32(-1074395981)
    ERR_COM_INITIALIZE                                       = _int32(-1074395980)
    ERR_INVALID_PARTICLE_INFO                                = _int32(-1074395979)
    ERR_INVALID_PARTICLE_NUMBER                              = _int32(-1074395978)
    ERR_AVI_VERSION                                          = _int32(-1074395977)
    ERR_NUMBER_OF_PALETTE_COLORS                             = _int32(-1074395976)
    ERR_AVI_TIMEOUT                                          = _int32(-1074395975)
    ERR_UNSUPPORTED_JPEG2000_COLORSPACE_METHOD               = _int32(-1074395974)
    ERR_JPEG2000_UNSUPPORTED_MULTIPLE_LAYERS                 = _int32(-1074395973)
    ERR_DIRECTX_ENUMERATE_FILTERS                            = _int32(-1074395972)
    ERR_INVALID_OFFSET                                       = _int32(-1074395971)
    ERR_AVI_OPEN                                             = _int32(-1074395970)
    ERR_AVI_CREATE                                           = _int32(-1074395969)
    ERR_AVI_WRITE                                            = _int32(-1074395968)
    ERR_AVI_READ                                             = _int32(-1074395967)
    ERR_AVI_IMAGE_CONVERSION                                 = _int32(-1074395966)
    ERR_AVI_MAX_SIZE_REACHED                                 = _int32(-1074395965)
    ERR_AVI_INVALID_CODEC_SOURCE                             = _int32(-1074395964)
    ERR_AVI_EXTENSION_REQUIRED                               = _int32(-1074395963)
    ERR_EMPTY_CODEC                                          = _int32(-1074395962)
    ERR_INIT                                                 = _int32(-1074395960)
    ERR_CREATE_WINDOW                                        = _int32(-1074395959)
    ERR_WINDOW_ID                                            = _int32(-1074395958)
    ERR_ARRAY_SIZE_MISMATCH                                  = _int32(-1074395957)
    ERR_INVALID_QUALITY                                      = _int32(-1074395956)
    ERR_INVALID_MAX_WAVELET_TRANSFORM_LEVEL                  = _int32(-1074395955)
    ERR_INVALID_QUANTIZATION_STEP_SIZE                       = _int32(-1074395954)
    ERR_INVALID_WAVELET_TRANSFORM_MODE                       = _int32(-1074395953)
    ERR_ROI_NOT_POINT                                        = _int32(-1074395952)
    ERR_ROI_NOT_POINTS                                       = _int32(-1074395951)
    ERR_ROI_NOT_LINE                                         = _int32(-1074395950)
    ERR_ROI_NOT_ANNULUS                                      = _int32(-1074395949)
    ERR_INVALID_MEASURE_PARTICLES_CALIBRATION_MODE           = _int32(-1074395948)
    ERR_INVALID_PARTICLE_CLASSIFIER_THRESHOLD_TYPE           = _int32(-1074395947)
    ERR_INVALID_DISTANCE                                     = _int32(-1074395946)
    ERR_INVALID_PARTICLE_AREA                                = _int32(-1074395945)
    ERR_CLASS_NAME_NOT_FOUND                                 = _int32(-1074395944)
    ERR_NUMBER_LABEL_LIMIT_EXCEEDED                          = _int32(-1074395943)
    ERR_INVALID_DISTANCE_LEVEL                               = _int32(-1074395942)
    ERR_INVALID_SVM_TYPE                                     = _int32(-1074395941)
    ERR_INVALID_SVM_KERNEL                                   = _int32(-1074395940)
    ERR_NO_SUPPORT_VECTOR_FOUND                              = _int32(-1074395939)
    ERR_COST_LABEL_NOT_FOUND                                 = _int32(-1074395938)
    ERR_EXCEEDED_SVM_MAX_ITERATION                           = _int32(-1074395937)
    ERR_INVALID_SVM_PARAMETER                                = _int32(-1074395936)
    ERR_INVALID_IDENTIFICATION_SCORE                         = _int32(-1074395935)
    ERR_INVALID_TEXTURE_FEATURE                              = _int32(-1074395934)
    ERR_INVALID_COOCCURRENCE_LEVEL                           = _int32(-1074395933)
    ERR_INVALID_WAVELET_SUBBAND                              = _int32(-1074395932)
    ERR_INVALID_FINAL_STEP_SIZE                              = _int32(-1074395931)
    ERR_INVALID_ENERGY                                       = _int32(-1074395930)
    ERR_INVALID_TEXTURE_LABEL                                = _int32(-1074395929)
    ERR_INVALID_WAVELET_TYPE                                 = _int32(-1074395928)
    ERR_SAME_WAVELET_BANDS_SELECTED                          = _int32(-1074395927)
    ERR_IMAGE_SIZE_MISMATCH                                  = _int32(-1074395926)
    ERR_INVALID_OBJECT_TRACKING_FILE                         = _int32(-1074395925)
    ERR_PYRAMID_LEVEL_NOT_VALID                              = _int32(-1074395924)
    ERR_INVALID_ANGLE_RANGE                                  = _int32(-1074395923)
    ERR_INVALID_LEARN_ANGLE_RANGE                            = _int32(-1074395922)
    ERR_OPENING_NEWER_OBJECT_TRACKING_REFNUM                 = _int32(-1074395921)
    ERR_NUMBER_CLASS                                         = _int32(-1074395920)
    ERR_INVALID_THRESHOLD_TYPE                               = _int32(-1074395919)
    ERR_MULTIPLE_LINE_DETECTION_NOT_ENABLED                  = _int32(-1074395918)
    ERR_OCR_INVALID_LINE_SEPARATOR                           = _int32(-1074395917)
    ERR_INVALID_OBJECT_POSITION                              = _int32(-1074395916)
    ERR_UNEQUAL_IMAGE_SIZE_FOR_OBJECT_ADDITION               = _int32(-1074395915)
    ERR_INVALID_INITIAL_ANGLE                                = _int32(-1074395914)
    ERR_UNINITIATED_SHAPE_ADAPTED_MEANSHIFT                  = _int32(-1074395913)
    ERR_UNINITIATED_MEANSHIFT                                = _int32(-1074395912)
    ERR_INVALID_MIN_SCORE                                    = _int32(-1074395911)
    ERR_INVALID_BOUNDINGBOX                                  = _int32(-1074395910)
    ERR_INVALID_COVARIANCEMATRIX                             = _int32(-1074395909)
    ERR_BAD_GAUSSIANKERNEL                                   = _int32(-1074395908)
    ERR_OBJECT_IS_LOST                                       = _int32(-1074395907)
    ERR_INVALID_HISTOGRAMSIZE                                = _int32(-1074395906)
    ERR_INVALID_HISTOGRAMTYPES                               = _int32(-1074395905)
    ERR_OBJECT_OUTSIDE_FRAME                                 = _int32(-1074395904)
    ERR_INVALID_HISTOGRAMBINS_FOR_COLOR_PROCESSING           = _int32(-1074395903)
    ERR_SUMHIST_UNEXPECTED                                   = _int32(-1074395902)
    ERR_INVALID_OBJECTTRACKING_REFNUM                        = _int32(-1074395901)
    ERR_NO_SHAPEADAPTEDMEANSHIFT_INSTANCE                    = _int32(-1074395900)
    ERR_NO_MEANSHIFT_INSTANCE                                = _int32(-1074395899)
    ERR_INVALID_OBJECT_TRACKING_INSTANCE_NUMBER              = _int32(-1074395898)
    ERR_INVALID_TRACKINGMEHOD                                = _int32(-1074395897)
    ERR_INVALID_BLOBTRACKING_INFO                            = _int32(-1074395896)
    ERR_UNINITIALIZED_OBJECTTRACKING_REFNUM                  = _int32(-1074395895)
    ERR_INVALID_INSTANCENUMBER                               = _int32(-1074395894)
    ERR_INVALID_MAXSHAPECHANGE                               = _int32(-1074395893)
    ERR_INVALID_MAXROTATIONCHANGE                            = _int32(-1074395892)
    ERR_INVALID_MAXSCALECHANGE                               = _int32(-1074395891)
    ERR_INVALID_NUMBER_OF_HISTOGRAMBINS                      = _int32(-1074395890)
    ERR_INVALID_BLENDINGPARAMETER                            = _int32(-1074395889)
    ERR_INVALID_LUCAS_KANADE_WINDOW_SIZE                     = _int32(-1074395888)
    ERR_INVALID_MATRIX_TYPE                                  = _int32(-1074395887)
    ERR_INVALID_OPTICAL_FLOW_TERMINATION_CRITERIA_TYPE       = _int32(-1074395886)
    ERR_LKP_NULL_PYRAMID                                     = _int32(-1074395885)
    ERR_INVALID_PYRAMID_LEVEL                                = _int32(-1074395884)
    ERR_INVALID_LKP_KERNEL                                   = _int32(-1074395883)
    ERR_INVALID_HORN_SCHUNCK_LAMBDA                          = _int32(-1074395882)
    ERR_INVALID_HORN_SCHUNCK_TYPE                            = _int32(-1074395881)
    ERR_PARTICLE                                             = _int32(-1074395880)
    ERR_BAD_MEASURE                                          = _int32(-1074395879)
    ERR_PROP_NODE_WRITE_NOT_SUPPORTED                        = _int32(-1074395878)
    ERR_COLORMODE_REQUIRES_CHANGECOLORSPACE2                 = _int32(-1074395877)
    ERR_UNSUPPORTED_COLOR_MODE                               = _int32(-1074395876)
    ERR_BARCODE_PHARMACODE                                   = _int32(-1074395875)
    ERR_EDVR_UNSUPPORTED_ARRAY_TYPE                          = _int32(-1074395874)
    ERR_EDVR_INCOMPATIBLE_ARRAY_TYPE                         = _int32(-1074395873)
    ERR_EDVR_INVALID_RECT_WIDTH                              = _int32(-1074395872)
    ERR_EDVR_INVALID_RECT_HEIGHT                             = _int32(-1074395871)
    ERR_EDVR_INVALID_XSTEP                                   = _int32(-1074395870)
    ERR_EDVR_INVALID_YSTEP                                   = _int32(-1074395869)
    ERR_INVALID_NUM_REQUIRED_BARCODES                        = _int32(-1074395868)
    ERR_INVALID_SIZE_FOR_DMA_FIFO_TRANSFER                   = _int32(-1074395867)
    ERR_MORE_THAN_1_MATCHING_CTL                             = _int32(-1074395866)
    ERR_MORE_THAN_1_MATCHING_DMA_FIFO                        = _int32(-1074395865)
    ERR_FIFO_DEPTH_IS_0                                      = _int32(-1074395864)
    ERR_NO_MATCHING_CTL                                      = _int32(-1074395863)
    ERR_NO_MATCHING_DMA_FIFO                                 = _int32(-1074395862)
    ERR_INVALID_MAX_PIXELS_PER_WRITE_OR_READ                 = _int32(-1074395861)
    ERR_INVALID_EDVR_DIMENSION                               = _int32(-1074395860)
    ERR_INVALID_IMAGE_OFFSET                                 = _int32(-1074395859)
    ERR_MISMATCHED_ELEMENT_SIZE                              = _int32(-1074395858)
    ERR_DISPLAY_COMMUNICATION                                = _int32(-1074395841)
    ERR_BAD_INDEX                                            = _int32(-1074395840)
    ERR_INVALID_COMPRESSION_RATIO                            = _int32(-1074395837)
    ERR_TOO_MANY_CONTOURS                                    = _int32(-1074395801)
    ERR_PROTECTION                                           = _int32(-1074395800)
    ERR_INTERNAL                                             = _int32(-1074395799)
    ERR_INVALID_CUSTOM_SAMPLE                                = _int32(-1074395798)
    ERR_INVALID_CLASSIFIER_SESSION                           = _int32(-1074395797)
    ERR_INVALID_KNN_METHOD                                   = _int32(-1074395796)
    ERR_K_TOO_LOW                                            = _int32(-1074395795)
    ERR_K_TOO_HIGH                                           = _int32(-1074395794)
    ERR_INVALID_OPERATION_ON_COMPACT_SESSION_ATTEMPTED       = _int32(-1074395793)
    ERR_CLASSIFIER_SESSION_NOT_TRAINED                       = _int32(-1074395792)
    ERR_CLASSIFIER_INVALID_SESSION_TYPE                      = _int32(-1074395791)
    ERR_INVALID_DISTANCE_METRIC                              = _int32(-1074395790)
    ERR_OPENING_NEWER_CLASSIFIER_SESSION                     = _int32(-1074395789)
    ERR_NO_SAMPLES                                           = _int32(-1074395788)
    ERR_INVALID_CLASSIFIER_TYPE                              = _int32(-1074395787)
    ERR_INVALID_PARTICLE_OPTIONS                             = _int32(-1074395786)
    ERR_NO_PARTICLE                                          = _int32(-1074395785)
    ERR_INVALID_LIMITS                                       = _int32(-1074395784)
    ERR_BAD_SAMPLE_INDEX                                     = _int32(-1074395783)
    ERR_DESCRIPTION_TOO_LONG                                 = _int32(-1074395782)
    ERR_CLASSIFIER_INVALID_ENGINE_TYPE                       = _int32(-1074395781)
    ERR_INVALID_PARTICLE_TYPE                                = _int32(-1074395780)
    ERR_CANNOT_COMPACT_UNTRAINED                             = _int32(-1074395779)
    ERR_INVALID_KERNEL_SIZE                                  = _int32(-1074395778)
    ERR_INCOMPATIBLE_CLASSIFIER_TYPES                        = _int32(-1074395777)
    ERR_INVALID_USE_OF_COMPACT_SESSION_FILE                  = _int32(-1074395776)
    ERR_ROI_HAS_OPEN_CONTOURS                                = _int32(-1074395775)
    ERR_NO_LABEL                                             = _int32(-1074395774)
    ERR_NO_DEST_IMAGE                                        = _int32(-1074395773)
    ERR_INVALID_REGISTRATION_METHOD                          = _int32(-1074395772)
    ERR_OPENING_NEWER_INSPECTION_TEMPLATE                    = _int32(-1074395771)
    ERR_INVALID_INSPECTION_TEMPLATE                          = _int32(-1074395770)
    ERR_INVALID_EDGE_THICKNESS                               = _int32(-1074395769)
    ERR_INVALID_SCALE                                        = _int32(-1074395768)
    ERR_INVALID_ALIGNMENT                                    = _int32(-1074395767)
    ERR_DEPRECATED_FUNCTION                                  = _int32(-1074395766)
    ERR_INVALID_NORMALIZATION_METHOD                         = _int32(-1074395763)
    ERR_INVALID_NIBLACK_DEVIATION_FACTOR                     = _int32(-1074395762)
    ERR_INVALID_SAUVOLA_DEVIATION_RANGE                      = _int32(-1074395761)
    ERR_BOARD_NOT_FOUND                                      = _int32(-1074395760)
    ERR_BOARD_NOT_OPEN                                       = _int32(-1074395758)
    ERR_DLL_NOT_FOUND                                        = _int32(-1074395757)
    ERR_DLL_FUNCTION_NOT_FOUND                               = _int32(-1074395756)
    ERR_TRIG_TIMEOUT                                         = _int32(-1074395754)
    ERR_CONTOUR_INVALID_REFINEMENTS                          = _int32(-1074395746)
    ERR_TOO_MANY_CURVES                                      = _int32(-1074395745)
    ERR_CONTOUR_INVALID_KERNEL_FOR_SMOOTHING                 = _int32(-1074395744)
    ERR_CONTOUR_LINE_INVALID                                 = _int32(-1074395743)
    ERR_CONTOUR_TEMPLATE_IMAGE_INVALID                       = _int32(-1074395742)
    ERR_CONTOUR_GPM_FAIL                                     = _int32(-1074395741)
    ERR_CONTOUR_OPENING_NEWER_VERSION                        = _int32(-1074395740)
    ERR_CONTOUR_CONNECT_DUPLICATE                            = _int32(-1074395739)
    ERR_CONTOUR_CONNECT_TYPE                                 = _int32(-1074395738)
    ERR_CONTOUR_MATCH_STR_NOT_APPLICABLE                     = _int32(-1074395737)
    ERR_CONTOUR_CURVATURE_KERNEL                             = _int32(-1074395736)
    ERR_CONTOUR_EXTRACT_SELECTION                            = _int32(-1074395735)
    ERR_CONTOUR_EXTRACT_DIRECTION                            = _int32(-1074395734)
    ERR_CONTOUR_EXTRACT_ROI                                  = _int32(-1074395733)
    ERR_CONTOUR_NO_CURVES                                    = _int32(-1074395732)
    ERR_CONTOUR_COMPARE_KERNEL                               = _int32(-1074395731)
    ERR_CONTOUR_COMPARE_SINGLE_IMAGE                         = _int32(-1074395730)
    ERR_CONTOUR_INVALID                                      = _int32(-1074395729)
    ERR_INVALID_2D_BARCODE_SEARCH_MODE                       = _int32(-1074395728)
    ERR_UNSUPPORTED_2D_BARCODE_SEARCH_MODE                   = _int32(-1074395727)
    ERR_MATCHFACTOR_OBSOLETE                                 = _int32(-1074395726)
    ERR_DATA_VERSION                                         = _int32(-1074395725)
    ERR_CUSTOMDATA_INVALID_SIZE                              = _int32(-1074395724)
    ERR_CUSTOMDATA_KEY_NOT_FOUND                             = _int32(-1074395723)
    ERR_CLASSIFIER_CLASSIFY_IMAGE_WITH_CUSTOM_SESSION        = _int32(-1074395722)
    ERR_INVALID_BIT_DEPTH                                    = _int32(-1074395721)
    ERR_BAD_ROI                                              = _int32(-1074395720)
    ERR_BAD_ROI_BOX                                          = _int32(-1074395719)
    ERR_LAB_VERSION                                          = _int32(-1074395718)
    ERR_INVALID_RANGE                                        = _int32(-1074395717)
    ERR_INVALID_SCALING_METHOD                               = _int32(-1074395716)
    ERR_INVALID_CALIBRATION_UNIT                             = _int32(-1074395715)
    ERR_INVALID_AXIS_ORIENTATION                             = _int32(-1074395714)
    ERR_VALUE_NOT_IN_ENUM                                    = _int32(-1074395713)
    ERR_WRONG_REGION_TYPE                                    = _int32(-1074395712)
    ERR_NOT_ENOUGH_REGIONS                                   = _int32(-1074395711)
    ERR_TOO_MANY_PARTICLES                                   = _int32(-1074395710)
    ERR_AVI_UNOPENED_SESSION                                 = _int32(-1074395709)
    ERR_AVI_READ_SESSION_REQUIRED                            = _int32(-1074395708)
    ERR_AVI_WRITE_SESSION_REQUIRED                           = _int32(-1074395707)
    ERR_AVI_SESSION_ALREADY_OPEN                             = _int32(-1074395706)
    ERR_DATA_CORRUPTED                                       = _int32(-1074395705)
    ERR_INVALID_COMPRESSION_TYPE                             = _int32(-1074395704)
    ERR_INVALID_TYPE_OF_FLATTEN                              = _int32(-1074395703)
    ERR_INVALID_LENGTH                                       = _int32(-1074395702)
    ERR_INVALID_MATRIX_SIZE_RANGE                            = _int32(-1074395701)
    ERR_REQUIRES_WIN2000_OR_NEWER                            = _int32(-1074395700)
    ERR_INVALID_CALIBRATION_METHOD                           = _int32(-1074395662)
    ERR_INVALID_OPERATION_ON_COMPACT_CALIBRATION_ATTEMPTED   = _int32(-1074395661)
    ERR_INVALID_POLYNOMIAL_MODEL_K_COUNT                     = _int32(-1074395660)
    ERR_INVALID_DISTORTION_MODEL                             = _int32(-1074395659)
    ERR_CAMERA_MODEL_NOT_AVAILABLE                           = _int32(-1074395658)
    ERR_INVALID_THUMBNAIL_INDEX                              = _int32(-1074395657)
    ERR_SMOOTH_CONTOURS_MUST_BE_SAME                         = _int32(-1074395656)
    ERR_ENABLE_CALIBRATION_SUPPORT_MUST_BE_SAME              = _int32(-1074395655)
    ERR_GRADING_INFORMATION_NOT_FOUND                        = _int32(-1074395654)
    ERR_OPENING_NEWER_MULTIPLE_GEOMETRIC_TEMPLATE            = _int32(-1074395653)
    ERR_OPENING_NEWER_GEOMETRIC_MATCHING_TEMPLATE            = _int32(-1074395652)
    ERR_EDGE_FILTER_SIZE_MUST_BE_SAME                        = _int32(-1074395651)
    ERR_CURVE_EXTRACTION_MODE_MUST_BE_SAME                   = _int32(-1074395650)
    ERR_INVALID_GEOMETRIC_FEATURE_TYPE                       = _int32(-1074395649)
    ERR_TEMPLATE_NOT_LEARNED                                 = _int32(-1074395648)
    ERR_INVALID_MULTIPLE_GEOMETRIC_TEMPLATE                  = _int32(-1074395647)
    ERR_NO_TEMPLATE_TO_LEARN                                 = _int32(-1074395646)
    ERR_INVALID_NUMBER_OF_LABELS                             = _int32(-1074395645)
    ERR_LABEL_TOO_LONG                                       = _int32(-1074395644)
    ERR_INVALID_NUMBER_OF_MATCH_OPTIONS                      = _int32(-1074395643)
    ERR_LABEL_NOT_FOUND                                      = _int32(-1074395642)
    ERR_DUPLICATE_LABEL                                      = _int32(-1074395641)
    ERR_TOO_MANY_ZONES                                       = _int32(-1074395640)
    ERR_INVALID_HATCH_STYLE                                  = _int32(-1074395639)
    ERR_INVALID_FILL_STYLE                                   = _int32(-1074395638)
    ERR_HARDWARE_DOESNT_SUPPORT_NONTEARING                   = _int32(-1074395637)
    ERR_DIRECTX_NOT_FOUND                                    = _int32(-1074395636)
    ERR_INVALID_SHAPE_DESCRIPTOR                             = _int32(-1074395635)
    ERR_INVALID_MAX_MATCH_OVERLAP                            = _int32(-1074395634)
    ERR_INVALID_MIN_MATCH_SEPARATION_SCALE                   = _int32(-1074395633)
    ERR_INVALID_MIN_MATCH_SEPARATION_ANGLE                   = _int32(-1074395632)
    ERR_INVALID_MIN_MATCH_SEPARATION_DISTANCE                = _int32(-1074395631)
    ERR_INVALID_MAXIMUM_FEATURES_LEARNED                     = _int32(-1074395630)
    ERR_INVALID_MAXIMUM_PIXEL_DISTANCE_FROM_LINE             = _int32(-1074395629)
    ERR_INVALID_GEOMETRIC_MATCHING_TEMPLATE                  = _int32(-1074395628)
    ERR_NOT_ENOUGH_TEMPLATE_FEATURES_1                       = _int32(-1074395627)
    ERR_NOT_ENOUGH_TEMPLATE_FEATURES                         = _int32(-1074395626)
    ERR_INVALID_MATCH_CONSTRAINT_TYPE                        = _int32(-1074395625)
    ERR_INVALID_OCCLUSION_RANGE                              = _int32(-1074395624)
    ERR_INVALID_SCALE_RANGE                                  = _int32(-1074395623)
    ERR_INVALID_MATCH_GEOMETRIC_PATTERN_SETUP_DATA           = _int32(-1074395622)
    ERR_INVALID_LEARN_GEOMETRIC_PATTERN_SETUP_DATA           = _int32(-1074395621)
    ERR_INVALID_CURVE_EXTRACTION_MODE                        = _int32(-1074395620)
    ERR_TOO_MANY_OCCLUSION_RANGES                            = _int32(-1074395619)
    ERR_TOO_MANY_SCALE_RANGES                                = _int32(-1074395618)
    ERR_INVALID_NUMBER_OF_FEATURES_RANGE                     = _int32(-1074395617)
    ERR_INVALID_EDGE_FILTER_SIZE                             = _int32(-1074395616)
    ERR_INVALID_MINIMUM_FEATURE_STRENGTH                     = _int32(-1074395615)
    ERR_INVALID_MINIMUM_FEATURE_ASPECT_RATIO                 = _int32(-1074395614)
    ERR_INVALID_MINIMUM_FEATURE_LENGTH                       = _int32(-1074395613)
    ERR_INVALID_MINIMUM_FEATURE_RADIUS                       = _int32(-1074395612)
    ERR_INVALID_MINIMUM_RECTANGLE_DIMENSION                  = _int32(-1074395611)
    ERR_INVALID_INITIAL_MATCH_LIST_LENGTH                    = _int32(-1074395610)
    ERR_INVALID_SUBPIXEL_TOLERANCE                           = _int32(-1074395609)
    ERR_INVALID_SUBPIXEL_ITERATIONS                          = _int32(-1074395608)
    ERR_INVALID_MAXIMUM_FEATURES_PER_MATCH                   = _int32(-1074395607)
    ERR_INVALID_MINIMUM_FEATURES_TO_MATCH                    = _int32(-1074395606)
    ERR_INVALID_MAXIMUM_END_POINT_GAP                        = _int32(-1074395605)
    ERR_INVALID_COLUMN_STEP                                  = _int32(-1074395604)
    ERR_INVALID_ROW_STEP                                     = _int32(-1074395603)
    ERR_INVALID_MINIMUM_CURVE_LENGTH                         = _int32(-1074395602)
    ERR_INVALID_EDGE_THRESHOLD                               = _int32(-1074395601)
    ERR_INFO_NOT_FOUND                                       = _int32(-1074395600)
    ERR_NIOCR_INVALID_ACCEPTANCE_LEVEL                       = _int32(-1074395598)
    ERR_NIOCR_NOT_A_VALID_SESSION                            = _int32(-1074395597)
    ERR_NIOCR_INVALID_CHARACTER_SIZE                         = _int32(-1074395596)
    ERR_NIOCR_INVALID_THRESHOLD_MODE                         = _int32(-1074395595)
    ERR_NIOCR_INVALID_SUBSTITUTION_CHARACTER                 = _int32(-1074395594)
    ERR_NIOCR_INVALID_NUMBER_OF_BLOCKS                       = _int32(-1074395593)
    ERR_NIOCR_INVALID_READ_STRATEGY                          = _int32(-1074395592)
    ERR_NIOCR_INVALID_CHARACTER_INDEX                        = _int32(-1074395591)
    ERR_NIOCR_INVALID_NUMBER_OF_VALID_CHARACTER_POSITIONS    = _int32(-1074395590)
    ERR_NIOCR_INVALID_LOW_THRESHOLD_VALUE                    = _int32(-1074395589)
    ERR_NIOCR_INVALID_HIGH_THRESHOLD_VALUE                   = _int32(-1074395588)
    ERR_NIOCR_INVALID_THRESHOLD_RANGE                        = _int32(-1074395587)
    ERR_NIOCR_INVALID_LOWER_THRESHOLD_LIMIT                  = _int32(-1074395586)
    ERR_NIOCR_INVALID_UPPER_THRESHOLD_LIMIT                  = _int32(-1074395585)
    ERR_NIOCR_INVALID_THRESHOLD_LIMITS                       = _int32(-1074395584)
    ERR_NIOCR_INVALID_MIN_CHAR_SPACING                       = _int32(-1074395583)
    ERR_NIOCR_INVALID_MAX_HORIZ_ELEMENT_SPACING              = _int32(-1074395582)
    ERR_NIOCR_INVALID_MAX_VERT_ELEMENT_SPACING               = _int32(-1074395581)
    ERR_NIOCR_INVALID_MIN_BOUNDING_RECT_WIDTH                = _int32(-1074395580)
    ERR_NIOCR_INVALID_ASPECT_RATIO                           = _int32(-1074395579)
    ERR_NIOCR_INVALID_CHARACTER_SET_FILE                     = _int32(-1074395578)
    ERR_NIOCR_CHARACTER_VALUE_CANNOT_BE_EMPTYSTRING          = _int32(-1074395577)
    ERR_NIOCR_CHARACTER_VALUE_TOO_LONG                       = _int32(-1074395576)
    ERR_NIOCR_INVALID_NUMBER_OF_EROSIONS                     = _int32(-1074395575)
    ERR_NIOCR_CHARACTER_SET_DESCRIPTION_TOO_LONG             = _int32(-1074395574)
    ERR_NIOCR_INVALID_CHARACTER_SET_FILE_VERSION             = _int32(-1074395573)
    ERR_NIOCR_INTEGER_VALUE_FOR_STRING_ATTRIBUTE             = _int32(-1074395572)
    ERR_NIOCR_GET_ONLY_ATTRIBUTE                             = _int32(-1074395571)
    ERR_NIOCR_INTEGER_VALUE_FOR_BOOLEAN_ATTRIBUTE            = _int32(-1074395570)
    ERR_NIOCR_INVALID_ATTRIBUTE                              = _int32(-1074395569)
    ERR_NIOCR_STRING_VALUE_FOR_INTEGER_ATTRIBUTE             = _int32(-1074395568)
    ERR_NIOCR_STRING_VALUE_FOR_BOOLEAN_ATTRIBUTE             = _int32(-1074395567)
    ERR_NIOCR_BOOLEAN_VALUE_FOR_INTEGER_ATTRIBUTE            = _int32(-1074395566)
    ERR_NIOCR_MUST_BE_SINGLE_CHARACTER                       = _int32(-1074395565)
    ERR_NIOCR_INVALID_PREDEFINED_CHARACTER                   = _int32(-1074395564)
    ERR_NIOCR_UNLICENSED                                     = _int32(-1074395563)
    ERR_NIOCR_BOOLEAN_VALUE_FOR_STRING_ATTRIBUTE             = _int32(-1074395562)
    ERR_NIOCR_INVALID_NUMBER_OF_CHARACTERS                   = _int32(-1074395561)
    ERR_NIOCR_INVALID_OBJECT_INDEX                           = _int32(-1074395560)
    ERR_NIOCR_INVALID_READ_OPTION                            = _int32(-1074395559)
    ERR_NIOCR_INVALID_CHARACTER_SIZE_RANGE                   = _int32(-1074395558)
    ERR_NIOCR_INVALID_BOUNDING_RECT_WIDTH_RANGE              = _int32(-1074395557)
    ERR_NIOCR_INVALID_BOUNDING_RECT_HEIGHT_RANGE             = _int32(-1074395556)
    ERR_NIOCR_INVALID_SPACING_RANGE                          = _int32(-1074395555)
    ERR_NIOCR_INVALID_READ_RESOLUTION                        = _int32(-1074395554)
    ERR_NIOCR_INVALID_MIN_BOUNDING_RECT_HEIGHT               = _int32(-1074395553)
    ERR_NIOCR_NOT_A_VALID_CHARACTER_SET                      = _int32(-1074395552)
    ERR_NIOCR_RENAME_REFCHAR                                 = _int32(-1074395551)
    ERR_NIOCR_INVALID_CHARACTER_VALUE                        = _int32(-1074395550)
    ERR_NIOCR_INVALID_NUMBER_OF_OBJECTS_TO_VERIFY            = _int32(-1074395549)
    ERR_NO_IMAGE_LESS_THAN_TWO                               = _int32(-1074395548)
    ERR_NO_IMAGE_LESS_THAN_THREE                             = _int32(-1074395547)
    ERR_FLAT_FIELD_INFO_NOT_AVAILABLE                        = _int32(-1074395546)
    ERR_FLATFIELD_AND_DARK_FIELD_NOT_AVAILABLE               = _int32(-1074395545)
    ERR_INVALID_PRESET_OPTION                                = _int32(-1074395544)
    ERR_INVALID_PRESET_FUNCTION                              = _int32(-1074395543)
    ERR_INVALID_ALGORITHM                                    = _int32(-1074395542)
    ERR_NO_LOOKUP_TABLE                                      = _int32(-1074395533)
    ERR_INVALID_METHOD                                       = _int32(-1074395532)
    ERR_INF_OR_NAN_PARAMETER_VALUE                           = _int32(-1074395448)
    ERR_INSUFFICIENT_COLOR_POINTS                            = _int32(-1074395447)
    ERR_COLOPOINT_PIXEL_IS_INVALID                           = _int32(-1074395446)
    ERR_TOO_FEW_MATCHES                                      = _int32(-1074395445)
    ERR_GRID_SIZES_TOO_LESS                                  = _int32(-1074395444)
    ERR_GRID_SIZES_TOO_LARGE                                 = _int32(-1074395443)
    ERR_SIZE_MISMATCH_FEATURES_AND_DESCRIPTORS               = _int32(-1074395442)
    ERR_MATCHING_DISTANCE_LESS_THAN_ZERO                     = _int32(-1074395441)
    ERR_NO_DESCRIPTORS                                       = _int32(-1074395440)
    ERR_NO_FEATURE_POINTS                                    = _int32(-1074395439)
    ERR_PYRAMID_LEVEL_LESS_THAN_ONE                          = _int32(-1074395438)
    ERR_MAX_CHAR_LENGTH_PER_LINE                             = _int32(-1074395437)
    ERR_INCOMP_IMAGE_SIZE_FOR_TRACKING                       = _int32(-1074395436)
    ERR_INVALID_MIN_OR_MAX_DEPTH_VALUE                       = _int32(-1074395435)
    ERR_INVALID_POLYNOMIAL_ORDER                             = _int32(-1074395434)
    ERR_INVALID_INTERPOLATION_SAMPLING_FREQUENCY             = _int32(-1074395433)
    ERR_INVALID_STEREO_INVALID_MIN_DEPTH                     = _int32(-1074395432)
    ERR_INVALID_STEREO_INVALID_DISPARITY_VALUE               = _int32(-1074395431)
    ERR_INVALID_STEREO_CAMERA_TRANSLATION                    = _int32(-1074395430)
    ERR_INVALID_STEREO_CAMERA_POSITION                       = _int32(-1074395429)
    ERR_INVALID_STEREO_BLOCKMATCHING_POSTFILTER_SPECKLERANGE = _int32(-1074395428)
    ERR_INVALID_STEREO_BLOCKMATCHING_POSTFILTER_SPECKLESIZE  = _int32(-1074395427)
    ERR_INVALID_STEREO_BLOCKMATCHING_POSTFILTER_TEXTURE      = _int32(-1074395426)
    ERR_INVALID_STEREO_BLOCKMATCHING_POSTFILTER_UNIQUENESS   = _int32(-1074395425)
    ERR_INVALID_MIN_DEPTH_VALUE                              = _int32(-1074395424)
    ERR_INVALID_STEREO_Q_MATRIX                              = _int32(-1074395423)
    ERR_INVALID_STEREO_SCALING_PARAMETER                     = _int32(-1074395422)
    ERR_INVALID_STEREO_BLOCKMATCHING_PREFILTER_CAP           = _int32(-1074395421)
    ERR_INVALID_STEREO_BLOCKMATCHING_PREFILTER_SIZE          = _int32(-1074395420)
    ERR_INVALID_STEREO_BLOCKMATCHING_PREFILTER_TYPE          = _int32(-1074395419)
    ERR_INVALID_STEREO_BLOCKMATCHING_NUMDISPARITIES          = _int32(-1074395418)
    ERR_INVALID_STEREO_BLOCKMATCHING_WINDOW_SIZE             = _int32(-1074395417)
    ERR_3DVISION_INVALID_SESSION_TYPE                        = _int32(-1074395416)
    ERR_TOO_MANY_3DVISION_SESSIONS                           = _int32(-1074395415)
    ERR_OPENING_NEWER_3DVISION_SESSION                       = _int32(-1074395414)
    ERR_INVALID_STEREO_BLOCKMATCHING_FILTERTYPE              = _int32(-1074395413)
    ERR_INVALID_3DVISION_SESSION                             = _int32(-1074395411)
    ERR_INVALID_ICONS_PER_LINE                               = _int32(-1074395410)
    ERR_INVALID_SUBPIXEL_DIVISIONS                           = _int32(-1074395409)
    ERR_INVALID_DETECTION_MODE                               = _int32(-1074395408)
    ERR_INVALID_CONTRAST                                     = _int32(-1074395407)
    ERR_COORDSYS_NOT_FOUND                                   = _int32(-1074395406)
    ERR_INVALID_TEXTORIENTATION                              = _int32(-1074395405)
    ERR_INVALID_INTERPOLATIONMETHOD_FOR_UNWRAP               = _int32(-1074395404)
    ERR_EXTRAINFO_VERSION                                    = _int32(-1074395403)
    ERR_INVALID_MAXPOINTS                                    = _int32(-1074395402)
    ERR_INVALID_MATCHFACTOR                                  = _int32(-1074395401)
    ERR_MULTICORE_OPERATION                                  = _int32(-1074395400)
    ERR_MULTICORE_INVALID_ARGUMENT                           = _int32(-1074395399)
    ERR_COMPLEX_IMAGE_REQUIRED                               = _int32(-1074395397)
    ERR_COLOR_IMAGE_REQUIRED                                 = _int32(-1074395395)
    ERR_COLOR_SPECTRUM_MASK                                  = _int32(-1074395394)
    ERR_COLOR_TEMPLATE_IMAGE_TOO_SMALL                       = _int32(-1074395393)
    ERR_COLOR_TEMPLATE_IMAGE_TOO_LARGE                       = _int32(-1074395392)
    ERR_COLOR_TEMPLATE_IMAGE_HUE_CONTRAST_TOO_LOW            = _int32(-1074395391)
    ERR_COLOR_TEMPLATE_IMAGE_LUMINANCE_CONTRAST_TOO_LOW      = _int32(-1074395390)
    ERR_COLOR_LEARN_SETUP_DATA                               = _int32(-1074395389)
    ERR_COLOR_LEARN_SETUP_DATA_SHAPE                         = _int32(-1074395388)
    ERR_COLOR_MATCH_SETUP_DATA                               = _int32(-1074395387)
    ERR_COLOR_MATCH_SETUP_DATA_SHAPE                         = _int32(-1074395386)
    ERR_COLOR_ROTATION_REQUIRES_SHAPE_FEATURE                = _int32(-1074395385)
    ERR_COLOR_TEMPLATE_DESCRIPTOR                            = _int32(-1074395384)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_1                          = _int32(-1074395383)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_2                          = _int32(-1074395382)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_3                          = _int32(-1074395381)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_4                          = _int32(-1074395380)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_5                          = _int32(-1074395379)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_6                          = _int32(-1074395378)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_SHIFT                      = _int32(-1074395377)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_NOSHIFT                    = _int32(-1074395376)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_SHIFT_1                    = _int32(-1074395375)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_SHIFT_2                    = _int32(-1074395374)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_ROTATION                   = _int32(-1074395373)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_NOROTATION                 = _int32(-1074395372)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_ROTATION_1                 = _int32(-1074395371)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_ROTATION_2                 = _int32(-1074395370)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_ROTATION_3                 = _int32(-1074395369)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_ROTATION_4                 = _int32(-1074395368)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_ROTATION_5                 = _int32(-1074395367)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_NOSHAPE                    = _int32(-1074395366)
    ERR_COLOR_TEMPLATE_DESCRIPTOR_NOSPECTRUM                 = _int32(-1074395365)
    ERR_IGNORE_COLOR_SPECTRUM_SET                            = _int32(-1074395364)
    ERR_INVALID_SUBSAMPLING_RATIO                            = _int32(-1074395363)
    ERR_INVALID_WIDTH                                        = _int32(-1074395362)
    ERR_INVALID_STEEPNESS                                    = _int32(-1074395361)
    ERR_COMPLEX_PLANE                                        = _int32(-1074395360)
    ERR_INVALID_COLOR_IGNORE_MODE                            = _int32(-1074395357)
    ERR_INVALID_MIN_MATCH_SCORE                              = _int32(-1074395356)
    ERR_INVALID_NUM_MATCHES_REQUESTED                        = _int32(-1074395355)
    ERR_INVALID_COLOR_WEIGHT                                 = _int32(-1074395354)
    ERR_INVALID_SEARCH_STRATEGY                              = _int32(-1074395353)
    ERR_INVALID_FEATURE_MODE                                 = _int32(-1074395352)
    ERR_INVALID_RECT                                         = _int32(-1074395351)
    ERR_INVALID_VISION_INFO                                  = _int32(-1074395350)
    ERR_INVALID_SKELETONMETHOD                               = _int32(-1074395349)
    ERR_INVALID_3DPLANE                                      = _int32(-1074395348)
    ERR_INVALID_3DDIRECTION                                  = _int32(-1074395347)
    ERR_INVALID_INTERPOLATIONMETHOD_FOR_ROTATE               = _int32(-1074395346)
    ERR_INVALID_FLIPAXIS                                     = _int32(-1074395345)
    ERR_FILE_FILENAME_NULL                                   = _int32(-1074395343)
    ERR_INVALID_SIZETYPE                                     = _int32(-1074395340)
    ERR_UNKNOWN_ALGORITHM                                    = _int32(-1074395336)
    ERR_DISPATCH_STATUS_CONFLICT                             = _int32(-1074395335)
    ERR_INVALID_CONVERSIONSTYLE                              = _int32(-1074395334)
    ERR_INVALID_VERTICAL_TEXT_ALIGNMENT                      = _int32(-1074395333)
    ERR_INVALID_COMPAREFUNCTION                              = _int32(-1074395332)
    ERR_INVALID_BORDERMETHOD                                 = _int32(-1074395331)
    ERR_INVALID_BORDER_SIZE                                  = _int32(-1074395330)
    ERR_INVALID_OUTLINEMETHOD                                = _int32(-1074395329)
    ERR_INVALID_INTERPOLATIONMETHOD                          = _int32(-1074395328)
    ERR_INVALID_SCALINGMODE                                  = _int32(-1074395327)
    ERR_INVALID_DRAWMODE_FOR_LINE                            = _int32(-1074395326)
    ERR_INVALID_DRAWMODE                                     = _int32(-1074395325)
    ERR_INVALID_SHAPEMODE                                    = _int32(-1074395324)
    ERR_INVALID_FONTCOLOR                                    = _int32(-1074395323)
    ERR_INVALID_TEXTALIGNMENT                                = _int32(-1074395322)
    ERR_INVALID_MORPHOLOGYMETHOD                             = _int32(-1074395321)
    ERR_TEMPLATE_EMPTY                                       = _int32(-1074395320)
    ERR_INVALID_SUBPIX_TYPE                                  = _int32(-1074395319)
    ERR_INSF_POINTS                                          = _int32(-1074395318)
    ERR_UNDEF_POINT                                          = _int32(-1074395317)
    ERR_INVALID_KERNEL_CODE                                  = _int32(-1074395316)
    ERR_INEFFICIENT_POINTS                                   = _int32(-1074395315)
    ERR_WRITE_FILE_NOT_SUPPORTED                             = _int32(-1074395313)
    ERR_LCD_CALIBRATE                                        = _int32(-1074395312)
    ERR_INVALID_COLOR_SPECTRUM                               = _int32(-1074395311)
    ERR_INVALID_PALETTE_TYPE                                 = _int32(-1074395310)
    ERR_INVALID_WINDOW_THREAD_POLICY                         = _int32(-1074395309)
    ERR_INVALID_COLORSENSITIVITY                             = _int32(-1074395308)
    ERR_PRECISION_NOT_GTR_THAN_0                             = _int32(-1074395307)
    ERR_INVALID_TOOL                                         = _int32(-1074395306)
    ERR_INVALID_REFERENCEMODE                                = _int32(-1074395305)
    ERR_INVALID_MATHTRANSFORMMETHOD                          = _int32(-1074395304)
    ERR_INVALID_NUM_OF_CLASSES                               = _int32(-1074395303)
    ERR_INVALID_THRESHOLDMETHOD                              = _int32(-1074395302)
    ERR_ROI_NOT_2_LINES                                      = _int32(-1074395301)
    ERR_INVALID_METERARCMODE                                 = _int32(-1074395300)
    ERR_INVALID_COMPLEXPLANE                                 = _int32(-1074395299)
    ERR_COMPLEXPLANE_NOT_REAL_OR_IMAGINARY                   = _int32(-1074395298)
    ERR_INVALID_PARTICLEINFOMODE                             = _int32(-1074395297)
    ERR_INVALID_BARCODETYPE                                  = _int32(-1074395296)
    ERR_INVALID_INTERPOLATIONMETHOD_INTERPOLATEPOINTS        = _int32(-1074395295)
    ERR_CONTOUR_INDEX_OUT_OF_RANGE                           = _int32(-1074395294)
    ERR_CONTOURID_NOT_FOUND                                  = _int32(-1074395293)
    ERR_POINTS_ARE_COLLINEAR                                 = _int32(-1074395292)
    ERR_SHAPEMATCH_BADIMAGEDATA                              = _int32(-1074395291)
    ERR_SHAPEMATCH_BADTEMPLATE                               = _int32(-1074395290)
    ERR_CONTAINER_CAPACITY_EXCEEDED_UINT_MAX                 = _int32(-1074395289)
    ERR_CONTAINER_CAPACITY_EXCEEDED_INT_MAX                  = _int32(-1074395288)
    ERR_INVALID_LINE                                         = _int32(-1074395287)
    ERR_INVALID_CONCENTRIC_RAKE_DIRECTION                    = _int32(-1074395286)
    ERR_INVALID_SPOKE_DIRECTION                              = _int32(-1074395285)
    ERR_INVALID_EDGE_PROCESS                                 = _int32(-1074395284)
    ERR_INVALID_RAKE_DIRECTION                               = _int32(-1074395283)
    ERR_CANT_DRAW_INTO_VIEWER                                = _int32(-1074395282)
    ERR_IMAGE_SMALLER_THAN_BORDER                            = _int32(-1074395281)
    ERR_ROI_NOT_RECT                                         = _int32(-1074395280)
    ERR_ROI_NOT_POLYGON                                      = _int32(-1074395279)
    ERR_LCD_NOT_NUMERIC                                      = _int32(-1074395278)
    ERR_BARCODE_CHECKSUM                                     = _int32(-1074395277)
    ERR_LINES_PARALLEL                                       = _int32(-1074395276)
    ERR_INVALID_BROWSER_IMAGE                                = _int32(-1074395275)
    ERR_DIV_BY_ZERO                                          = _int32(-1074395270)
    ERR_NULL_POINTER                                         = _int32(-1074395269)
    ERR_LINEAR_COEFF                                         = _int32(-1074395268)
    ERR_COMPLEX_ROOT                                         = _int32(-1074395267)
    ERR_BARCODE                                              = _int32(-1074395265)
    ERR_LCD_NO_SEGMENTS                                      = _int32(-1074395263)
    ERR_LCD_BAD_MATCH                                        = _int32(-1074395262)
    ERR_GIP_RANGE                                            = _int32(-1074395261)
    ERR_HEAP_TRASHED                                         = _int32(-1074395260)
    ERR_BAD_FILTER_WIDTH                                     = _int32(-1074395258)
    ERR_INVALID_EDGE_DIR                                     = _int32(-1074395257)
    ERR_EVEN_WINDOW_SIZE                                     = _int32(-1074395256)
    ERR_INVALID_LEARN_MODE                                   = _int32(-1074395253)
    ERR_LEARN_SETUP_DATA                                     = _int32(-1074395252)
    ERR_INVALID_MATCH_MODE                                   = _int32(-1074395251)
    ERR_MATCH_SETUP_DATA                                     = _int32(-1074395250)
    ERR_ROTATION_ANGLE_RANGE_TOO_LARGE                       = _int32(-1074395249)
    ERR_TOO_MANY_ROTATION_ANGLE_RANGES                       = _int32(-1074395248)
    ERR_TEMPLATE_DESCRIPTOR                                  = _int32(-1074395247)
    ERR_TEMPLATE_DESCRIPTOR_1                                = _int32(-1074395246)
    ERR_TEMPLATE_DESCRIPTOR_2                                = _int32(-1074395245)
    ERR_TEMPLATE_DESCRIPTOR_3                                = _int32(-1074395244)
    ERR_TEMPLATE_DESCRIPTOR_4                                = _int32(-1074395243)
    ERR_TEMPLATE_DESCRIPTOR_ROTATION                         = _int32(-1074395242)
    ERR_TEMPLATE_DESCRIPTOR_NOROTATION                       = _int32(-1074395241)
    ERR_TEMPLATE_DESCRIPTOR_ROTATION_1                       = _int32(-1074395240)
    ERR_TEMPLATE_DESCRIPTOR_SHIFT                            = _int32(-1074395239)
    ERR_TEMPLATE_DESCRIPTOR_NOSHIFT                          = _int32(-1074395238)
    ERR_TEMPLATE_DESCRIPTOR_SHIFT_1                          = _int32(-1074395237)
    ERR_TEMPLATE_DESCRIPTOR_NOSCALE                          = _int32(-1074395236)
    ERR_TEMPLATE_IMAGE_CONTRAST_TOO_LOW                      = _int32(-1074395235)
    ERR_TEMPLATE_IMAGE_TOO_SMALL                             = _int32(-1074395234)
    ERR_TEMPLATE_IMAGE_TOO_LARGE                             = _int32(-1074395233)
    ERR_WEIGHT_MAP_INVALID_IMAGE_TYPE                        = _int32(-1074395219)
    ERR_NO_MATCH_FOUND_TO_CALCULATE_DEFECT_MAP               = _int32(-1074395218)
    ERR_INVALID_NUM_DEFECT_IMAGES_IN                         = _int32(-1074395217)
    ERR_DEFECT_MAP_INFORMATION_NOT_FOUND                     = _int32(-1074395216)
    ERR_OPENING_NEWER_DEFECT_MAP_DATA                        = _int32(-1074395215)
    ERR_TOO_MANY_OCR_SESSIONS                                = _int32(-1074395214)
    ERR_OCR_TEMPLATE_WRONG_SIZE                              = _int32(-1074395212)
    ERR_OCR_BAD_TEXT_TEMPLATE                                = _int32(-1074395211)
    ERR_OCR_CANNOT_MATCH_TEXT_TEMPLATE                       = _int32(-1074395210)
    ERR_ECC_CODE_NOT_SUPPORTED                               = _int32(-1074395208)
    ERR_INVALID_GRADING_REFLECTANCE_PARAMETER                = _int32(-1074395207)
    ERR_OCR_LIB_INIT                                         = _int32(-1074395203)
    ERR_OCR_LOAD_LIBRARY                                     = _int32(-1074395201)
    ERR_OCR_INVALID_PARAMETER                                = _int32(-1074395200)
    ERR_MARKER_INFORMATION_NOT_SUPPLIED                      = _int32(-1074395199)
    ERR_INCOMPATIBLE_MARKER_IMAGE_SIZE                       = _int32(-1074395198)
    ERR_BOTH_MARKER_INPUTS_SUPPLIED                          = _int32(-1074395197)
    ERR_INVALID_MORPHOLOGICAL_OPERATION                      = _int32(-1074395196)
    ERR_IMAGE_CONTAINS_NAN_VALUES                            = _int32(-1074395195)
    ERR_OVERLAY_EXTRAINFO_OPENING_NEW_VERSION                = _int32(-1074395194)
    ERR_NO_CLAMP_FOUND                                       = _int32(-1074395193)
    ERR_NO_CLAMP_WITHIN_ANGLE_RANGE                          = _int32(-1074395192)
    ERR_GHT_INVALID_USE_ALL_CURVES_VALUE                     = _int32(-1074395188)
    ERR_INVALID_GAUSS_SIGMA_VALUE                            = _int32(-1074395187)
    ERR_INVALID_GAUSS_FILTER_TYPE                            = _int32(-1074395186)
    ERR_INVALID_CONTRAST_REVERSAL_MODE                       = _int32(-1074395185)
    ERR_INVALID_ROTATION_RANGE                               = _int32(-1074395184)
    ERR_GHT_INVALID_MINIMUM_LEARN_ANGLE_VALUE                = _int32(-1074395183)
    ERR_GHT_INVALID_MAXIMUM_LEARN_ANGLE_VALUE                = _int32(-1074395182)
    ERR_GHT_INVALID_MAXIMUM_LEARN_SCALE_FACTOR               = _int32(-1074395181)
    ERR_GHT_INVALID_MINIMUM_LEARN_SCALE_FACTOR               = _int32(-1074395180)
    ERR_OCR_PREPROCESSING_FAILED                             = _int32(-1074395179)
    ERR_OCR_RECOGNITION_FAILED                               = _int32(-1074395178)
    ERR_OCR_BAD_USER_DICTIONARY                              = _int32(-1074395175)
    ERR_OCR_INVALID_AUTOORIENTMODE                           = _int32(-1074395174)
    ERR_OCR_INVALID_LANGUAGE                                 = _int32(-1074395173)
    ERR_OCR_INVALID_CHARACTERSET                             = _int32(-1074395172)
    ERR_OCR_INI_FILE_NOT_FOUND                               = _int32(-1074395171)
    ERR_OCR_INVALID_CHARACTERTYPE                            = _int32(-1074395170)
    ERR_OCR_INVALID_RECOGNITIONMODE                          = _int32(-1074395169)
    ERR_OCR_INVALID_AUTOCORRECTIONMODE                       = _int32(-1074395168)
    ERR_OCR_INVALID_OUTPUTDELIMITER                          = _int32(-1074395167)
    ERR_OCR_BIN_DIR_NOT_FOUND                                = _int32(-1074395166)
    ERR_OCR_WTS_DIR_NOT_FOUND                                = _int32(-1074395165)
    ERR_OCR_ADD_WORD_FAILED                                  = _int32(-1074395164)
    ERR_OCR_INVALID_CHARACTERPREFERENCE                      = _int32(-1074395163)
    ERR_OCR_INVALID_CORRECTIONMODE                           = _int32(-1074395162)
    ERR_OCR_INVALID_CORRECTIONLEVEL                          = _int32(-1074395161)
    ERR_OCR_INVALID_MAXPOINTSIZE                             = _int32(-1074395160)
    ERR_OCR_INVALID_TOLERANCE                                = _int32(-1074395159)
    ERR_OCR_INVALID_CONTRASTMODE                             = _int32(-1074395158)
    ERR_OCR_SKEW_DETECT_FAILED                               = _int32(-1074395156)
    ERR_OCR_ORIENT_DETECT_FAILED                             = _int32(-1074395155)
    ERR_FONT_FILE_FORMAT                                     = _int32(-1074395153)
    ERR_FONT_FILE_NOT_FOUND                                  = _int32(-1074395152)
    ERR_OCR_CORRECTION_FAILED                                = _int32(-1074395151)
    ERR_INVALID_ROUNDING_MODE                                = _int32(-1074395150)
    ERR_DUPLICATE_TRANSFORM_TYPE                             = _int32(-1074395149)
    ERR_OVERLAY_GROUP_NOT_FOUND                              = _int32(-1074395148)
    ERR_BARCODE_RSSLIMITED                                   = _int32(-1074395147)
    ERR_QR_DETECTION_VERSION                                 = _int32(-1074395146)
    ERR_QR_INVALID_READ                                      = _int32(-1074395145)
    ERR_QR_INVALID_BARCODE                                   = _int32(-1074395144)
    ERR_QR_DETECTION_MODE                                    = _int32(-1074395143)
    ERR_QR_DETECTION_MODELTYPE                               = _int32(-1074395142)
    ERR_OCR_NO_TEXT_FOUND                                    = _int32(-1074395141)
    ERR_OCR_CHAR_REPORT_CORRUPTED                            = _int32(-1074395140)
    ERR_IMAQ_QR_DIMENSION_INVALID                            = _int32(-1074395139)
    ERR_OCR_REGION_TOO_SMALL                                 = _int32(-1074395138)
    ERR_BAYER_INVALID_ALGORITHM                              = _int32(-1074395135)
    ERR_BAYER_INVALID_PATTERN                                = _int32(-1074395134)
    ERR_BAYER_INVALID_RED_GAIN                               = _int32(-1074395133)
    ERR_BAYER_INVALID_GREEN_GAIN                             = _int32(-1074395132)
    ERR_BAYER_INVALID_BLUE_GAIN                              = _int32(-1074395131)
    ERR_TARGET_NO_SUPPORT                                    = _int32(-1074395130)
    ERR_IP_VARIANT_NOT_SUPPORTED                             = _int32(-1074395129)
    _FIRST_ERR                                               = _int32(-1074396160)
    _LAST_ERR                                                = _int32(-1074395129)
dERR={a.name:a.value for a in ERR}
drERR={a.value:a.name for a in ERR}





##### TYPE DEFINITIONS #####


BYTE=ctypes.c_ubyte
PBYTE=ctypes.POINTER(BYTE)
CHAR=ctypes.c_char
PCHAR=ctypes.c_char_p
UCHAR=ctypes.c_ubyte
PUCHAR=ctypes.POINTER(UCHAR)
ULONG_PTR=ctypes.c_uint64
LONG_PTR=ctypes.c_int64
WORD=ctypes.c_ushort
LPWORD=ctypes.POINTER(WORD)
LONGLONG=ctypes.c_int64
LPLONG=ctypes.POINTER(ctypes.c_long)
__int64=ctypes.c_int64
HANDLE=ctypes.c_void_p
LPHANDLE=ctypes.POINTER(HANDLE)
HWND=ctypes.c_void_p
HGLOBAL=ctypes.c_void_p
HINSTANCE=ctypes.c_void_p
HDC=ctypes.c_void_p
HMODULE=ctypes.c_void_p
HKEY=ctypes.c_void_p
PVOID=ctypes.c_void_p
LPVOID=ctypes.c_void_p
MirEGLNativeWindowType=ctypes.c_void_p
MirEGLNativeDisplayType=ctypes.c_void_p
class Plane3D(enum.IntEnum):
    IMAQ_3D_REAL            =_int32(0)
    IMAQ_3D_IMAGINARY       =_int32(1)
    IMAQ_3D_MAGNITUDE       =_int32(2)
    IMAQ_3D_PHASE           =_int32(3)
    IMAQ_PLANE_3D_SIZE_GUARD=_int32(0xFFFFFFFF)
dPlane3D={a.name:a.value for a in Plane3D}
drPlane3D={a.value:a.name for a in Plane3D}


class MeasurementValue(enum.IntEnum):
    IMAQ_AREA                        =_int32(0)
    IMAQ_AREA_CALIBRATED             =_int32(1)
    IMAQ_NUM_HOLES                   =_int32(2)
    IMAQ_AREA_OF_HOLES               =_int32(3)
    IMAQ_TOTAL_AREA                  =_int32(4)
    IMAQ_IMAGE_AREA                  =_int32(5)
    IMAQ_PARTICLE_TO_IMAGE           =_int32(6)
    IMAQ_PARTICLE_TO_TOTAL           =_int32(7)
    IMAQ_CENTER_MASS_X               =_int32(8)
    IMAQ_CENTER_MASS_Y               =_int32(9)
    IMAQ_LEFT_COLUMN                 =_int32(10)
    IMAQ_TOP_ROW                     =_int32(11)
    IMAQ_RIGHT_COLUMN                =_int32(12)
    IMAQ_BOTTOM_ROW                  =_int32(13)
    IMAQ_WIDTH                       =_int32(14)
    IMAQ_HEIGHT                      =_int32(15)
    IMAQ_MAX_SEGMENT_LENGTH          =_int32(16)
    IMAQ_MAX_SEGMENT_LEFT_COLUMN     =_int32(17)
    IMAQ_MAX_SEGMENT_TOP_ROW         =_int32(18)
    IMAQ_PERIMETER                   =_int32(19)
    IMAQ_PERIMETER_OF_HOLES          =_int32(20)
    IMAQ_SIGMA_X                     =_int32(21)
    IMAQ_SIGMA_Y                     =_int32(22)
    IMAQ_SIGMA_XX                    =_int32(23)
    IMAQ_SIGMA_YY                    =_int32(24)
    IMAQ_SIGMA_XY                    =_int32(25)
    IMAQ_PROJ_X                      =_int32(26)
    IMAQ_PROJ_Y                      =_int32(27)
    IMAQ_INERTIA_XX                  =_int32(28)
    IMAQ_INERTIA_YY                  =_int32(29)
    IMAQ_INERTIA_XY                  =_int32(30)
    IMAQ_MEAN_H                      =_int32(31)
    IMAQ_MEAN_V                      =_int32(32)
    IMAQ_MAX_INTERCEPT               =_int32(33)
    IMAQ_MEAN_INTERCEPT              =_int32(34)
    IMAQ_ORIENTATION                 =_int32(35)
    IMAQ_EQUIV_ELLIPSE_MINOR         =_int32(36)
    IMAQ_ELLIPSE_MAJOR               =_int32(37)
    IMAQ_ELLIPSE_MINOR               =_int32(38)
    IMAQ_ELLIPSE_RATIO               =_int32(39)
    IMAQ_RECT_LONG_SIDE              =_int32(40)
    IMAQ_RECT_SHORT_SIDE             =_int32(41)
    IMAQ_RECT_RATIO                  =_int32(42)
    IMAQ_ELONGATION                  =_int32(43)
    IMAQ_COMPACTNESS                 =_int32(44)
    IMAQ_HEYWOOD                     =_int32(45)
    IMAQ_TYPE_FACTOR                 =_int32(46)
    IMAQ_HYDRAULIC                   =_int32(47)
    IMAQ_WADDLE_DISK                 =_int32(48)
    IMAQ_DIAGONAL                    =_int32(49)
    IMAQ_MEASUREMENT_VALUE_SIZE_GUARD=_int32(0xFFFFFFFF)
dMeasurementValue={a.name:a.value for a in MeasurementValue}
drMeasurementValue={a.value:a.name for a in MeasurementValue}


class ScalingMethod(enum.IntEnum):
    IMAQ_SCALE_TO_PRESERVE_AREA   =_int32(0)
    IMAQ_SCALE_TO_FIT             =_int32(1)
    IMAQ_SCALING_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dScalingMethod={a.name:a.value for a in ScalingMethod}
drScalingMethod={a.value:a.name for a in ScalingMethod}


class ReferenceMode(enum.IntEnum):
    IMAQ_COORD_X_Y                =_int32(0)
    IMAQ_COORD_ORIGIN_X           =_int32(1)
    IMAQ_REFERENCE_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dReferenceMode={a.name:a.value for a in ReferenceMode}
drReferenceMode={a.value:a.name for a in ReferenceMode}


class RectOrientation(enum.IntEnum):
    IMAQ_BASE_INSIDE                =_int32(0)
    IMAQ_BASE_OUTSIDE               =_int32(1)
    IMAQ_TEXT_ORIENTATION_SIZE_GUARD=_int32(0xFFFFFFFF)
dRectOrientation={a.name:a.value for a in RectOrientation}
drRectOrientation={a.value:a.name for a in RectOrientation}


class RakeDirection(enum.IntEnum):
    IMAQ_LEFT_TO_RIGHT            =_int32(0)
    IMAQ_RIGHT_TO_LEFT            =_int32(1)
    IMAQ_TOP_TO_BOTTOM            =_int32(2)
    IMAQ_BOTTOM_TO_TOP            =_int32(3)
    IMAQ_RAKE_DIRECTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dRakeDirection={a.name:a.value for a in RakeDirection}
drRakeDirection={a.value:a.name for a in RakeDirection}


class SearchStrategy(enum.IntEnum):
    IMAQ_CONSERVATIVE              =_int32(1)
    IMAQ_BALANCED                  =_int32(2)
    IMAQ_AGGRESSIVE                =_int32(3)
    IMAQ_VERY_AGGRESSIVE           =_int32(4)
    IMAQ_SEARCH_STRATEGY_SIZE_GUARD=_int32(0xFFFFFFFF)
dSearchStrategy={a.name:a.value for a in SearchStrategy}
drSearchStrategy={a.value:a.name for a in SearchStrategy}


class LearnSetupOption(enum.IntEnum):
    IMAQ_LDLO_SearchStrategy                        =_int32(0)
    IMAQ_LDLO_InitialStepSize                       =_int32(1)
    IMAQ_LDLO_InitialSampleSize                     =_int32(2)
    IMAQ_LDLO_InitialSampleSizeFactor               =_int32(3)
    IMAQ_LDLO_InitialAngularAccuracy                =_int32(4)
    IMAQ_LDLO_FinalSampleSize                       =_int32(5)
    IMAQ_LDLO_FinalSampleSizeFactor                 =_int32(6)
    IMAQ_LDLO_FinalAngularAccuracy                  =_int32(7)
    IMAQ_LDLO_SubpixelSampleSize                    =_int32(8)
    IMAQ_LDLO_SubpixelSampleSizeFactor              =_int32(9)
    IMAQ_LDLO_MatchOffsetXPosition                  =_int32(10)
    IMAQ_LDLO_MatchOffsetYPosition                  =_int32(11)
    IMAQ_LDLO_MatchOffsetAngle                      =_int32(12)
    IMAQ_PYLO_SubpixelSampleSize                    =_int32(100)
    IMAQ_PYLO_SubpixelSampleSizeFactor              =_int32(101)
    IMAQ_PYLO_MatchOffsetXPosition                  =_int32(102)
    IMAQ_PYLO_MatchOffsetYPosition                  =_int32(103)
    IMAQ_PYLO_MatchOffsetAngle                      =_int32(104)
    IMAQ_PYLO_MaxPyramidLevelToStoreData            =_int32(105)
    IMAQ_PYLO_PreProcess                            =_int32(106)
    IMAQ_PYLO_PercentPixelsToKeepForGradientTemplate=_int32(107)
    IMAQ_COMBINEDLEARNSETUPOPTION_SIZE_GUARD        =_int32(0xFFFFFFFF)
dLearnSetupOption={a.name:a.value for a in LearnSetupOption}
drLearnSetupOption={a.value:a.name for a in LearnSetupOption}


class MatchSetupOption(enum.IntEnum):
    IMAQ_LDMO_MinimumContrast                         =_int32(0)
    IMAQ_LDMO_EnableSubpixelAccuracy                  =_int32(1)
    IMAQ_LDMO_SearchStrategy                          =_int32(2)
    IMAQ_LDMO_SubpixelIterations                      =_int32(3)
    IMAQ_LDMO_SubpixelTolerance                       =_int32(4)
    IMAQ_LDMO_InitialMatchListLength                  =_int32(5)
    IMAQ_LDMO_MatchListReductionFactor                =_int32(6)
    IMAQ_LDMO_InitialStepSize                         =_int32(7)
    IMAQ_LDMO_IntermediateAngularAccuracy             =_int32(8)
    IMAQ_PYMO_MaxPyramidLevel                         =_int32(100)
    IMAQ_PYMO_MinimumContrast                         =_int32(102)
    IMAQ_PYMO_EnableSubpixelAccuracy                  =_int32(103)
    IMAQ_PYMO_SubpixelIterations                      =_int32(104)
    IMAQ_PYMO_SubpixelTolerance                       =_int32(105)
    IMAQ_PYMO_InitialMatchListLength                  =_int32(106)
    IMAQ_PYMO_MatchListReductionFactor                =_int32(107)
    IMAQ_PYMO_IntermediateAngularAccuracy             =_int32(108)
    IMAQ_PYMO_ProcessBorderMatches                    =_int32(109)
    IMAQ_PYMO_MinMatchSeparationDistance              =_int32(111)
    IMAQ_PYMO_MinMatchSeparationAngle                 =_int32(112)
    IMAQ_PYMO_MaxMatchOverlap                         =_int32(113)
    IMAQ_PYMO_MaxCacheSizeInMegabytes                 =_int32(114)
    IMAQ_PYMO_ClearCacheOnEveryMatch                  =_int32(115)
    IMAQ_PYMO_EnableAccurateScoreComputatation        =_int32(116)
    IMAQ_PYMO_InterpolationForAccurateScoreComputation=_int32(117)
    IMAQ_PYMO_TargetToTemplateScore                   =_int32(118)
    IMAQ_ALLMO_EnableScoreMap                         =_int32(200)
    IMAQ_COMBINEDMATCHSETUPOPTION_IS_AN_INT           =_int32(0xFFFFFFFF)
dMatchSetupOption={a.name:a.value for a in MatchSetupOption}
drMatchSetupOption={a.value:a.name for a in MatchSetupOption}


class PointSymbol(enum.IntEnum):
    IMAQ_POINT_AS_PIXEL         =_int32(0)
    IMAQ_POINT_AS_CROSS         =_int32(1)
    IMAQ_POINT_USER_DEFINED     =_int32(2)
    IMAQ_POINT_SYMBOL_SIZE_GUARD=_int32(0xFFFFFFFF)
dPointSymbol={a.name:a.value for a in PointSymbol}
drPointSymbol={a.value:a.name for a in PointSymbol}


class ShapeMode(enum.IntEnum):
    IMAQ_SHAPE_RECT           =_int32(1)
    IMAQ_SHAPE_OVAL           =_int32(2)
    IMAQ_SHAPE_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dShapeMode={a.name:a.value for a in ShapeMode}
drShapeMode={a.value:a.name for a in ShapeMode}


class PhotometricMode(enum.IntEnum):
    IMAQ_WHITE_IS_ZERO              =_int32(0)
    IMAQ_BLACK_IS_ZERO              =_int32(1)
    IMAQ_PHOTOMETRIC_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dPhotometricMode={a.name:a.value for a in PhotometricMode}
drPhotometricMode={a.value:a.name for a in PhotometricMode}


class AttenuateMode(enum.IntEnum):
    IMAQ_ATTENUATE_LOW            =_int32(0)
    IMAQ_ATTENUATE_HIGH           =_int32(1)
    IMAQ_ATTENUATE_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dAttenuateMode={a.name:a.value for a in AttenuateMode}
drAttenuateMode={a.value:a.name for a in AttenuateMode}


class PaletteType(enum.IntEnum):
    IMAQ_PALETTE_GRAY           =_int32(0)
    IMAQ_PALETTE_BINARY         =_int32(1)
    IMAQ_PALETTE_GRADIENT       =_int32(2)
    IMAQ_PALETTE_RAINBOW        =_int32(3)
    IMAQ_PALETTE_TEMPERATURE    =_int32(4)
    IMAQ_PALETTE_USER           =_int32(5)
    IMAQ_PALETTE_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dPaletteType={a.name:a.value for a in PaletteType}
drPaletteType={a.value:a.name for a in PaletteType}


class ObjectType(enum.IntEnum):
    IMAQ_BRIGHT_OBJECTS        =_int32(0)
    IMAQ_DARK_OBJECTS          =_int32(1)
    IMAQ_OBJECT_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dObjectType={a.name:a.value for a in ObjectType}
drObjectType={a.value:a.name for a in ObjectType}


class MorphologyMethod(enum.IntEnum):
    IMAQ_AUTOM                       =_int32(0)
    IMAQ_CLOSE                       =_int32(1)
    IMAQ_DILATE                      =_int32(2)
    IMAQ_ERODE                       =_int32(3)
    IMAQ_GRADIENT                    =_int32(4)
    IMAQ_GRADIENTOUT                 =_int32(5)
    IMAQ_GRADIENTIN                  =_int32(6)
    IMAQ_HITMISS                     =_int32(7)
    IMAQ_OPEN                        =_int32(8)
    IMAQ_PCLOSE                      =_int32(9)
    IMAQ_POPEN                       =_int32(10)
    IMAQ_THICK                       =_int32(11)
    IMAQ_THIN                        =_int32(12)
    IMAQ_MORPHOLOGY_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dMorphologyMethod={a.name:a.value for a in MorphologyMethod}
drMorphologyMethod={a.value:a.name for a in MorphologyMethod}


class MeterArcMode(enum.IntEnum):
    IMAQ_METER_ARC_ROI            =_int32(0)
    IMAQ_METER_ARC_POINTS         =_int32(1)
    IMAQ_METER_ARC_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dMeterArcMode={a.name:a.value for a in MeterArcMode}
drMeterArcMode={a.value:a.name for a in MeterArcMode}


class PolarityType(enum.IntEnum):
    IMAQ_EDGE_FALLING            =_int32((-1))
    IMAQ_EDGE_RISING             =_int32(1)
    IMAQ_POLARITY_TYPE_SIZE_GUARD=_int32(0x7FFFFFFF)
dPolarityType={a.name:a.value for a in PolarityType}
drPolarityType={a.value:a.name for a in PolarityType}


class Tool(enum.IntEnum):
    IMAQ_NO_TOOL             =_int32((-1))
    IMAQ_SELECTION_TOOL      =_int32(0)
    IMAQ_POINT_TOOL          =_int32(1)
    IMAQ_LINE_TOOL           =_int32(2)
    IMAQ_RECTANGLE_TOOL      =_int32(3)
    IMAQ_OVAL_TOOL           =_int32(4)
    IMAQ_POLYGON_TOOL        =_int32(5)
    IMAQ_CLOSED_FREEHAND_TOOL=_int32(6)
    IMAQ_ANNULUS_TOOL        =_int32(7)
    IMAQ_ZOOM_TOOL           =_int32(8)
    IMAQ_PAN_TOOL            =_int32(9)
    IMAQ_POLYLINE_TOOL       =_int32(10)
    IMAQ_FREEHAND_TOOL       =_int32(11)
    IMAQ_ROTATED_RECT_TOOL   =_int32(12)
    IMAQ_ZOOM_OUT_TOOL       =_int32(13)
    IMAQ_TOOL_SIZE_GUARD     =_int32(0x7FFFFFFF)
dTool={a.name:a.value for a in Tool}
drTool={a.value:a.name for a in Tool}


class WindowThreadPolicy(enum.IntEnum):
    IMAQ_CALLING_THREAD                 =_int32(0)
    IMAQ_SEPARATE_THREAD                =_int32(1)
    IMAQ_WINDOW_THREAD_POLICY_SIZE_GUARD=_int32(0xFFFFFFFF)
dWindowThreadPolicy={a.name:a.value for a in WindowThreadPolicy}
drWindowThreadPolicy={a.value:a.name for a in WindowThreadPolicy}


class WindowOptions(enum.IntEnum):
    IMAQ_WIND_RESIZABLE           =_int32(1)
    IMAQ_WIND_TITLEBAR            =_int32(2)
    IMAQ_WIND_CLOSEABLE           =_int32(4)
    IMAQ_WIND_TOPMOST             =_int32(8)
    IMAQ_WINDOW_OPTIONS_SIZE_GUARD=_int32(0xFFFFFFFF)
dWindowOptions={a.name:a.value for a in WindowOptions}
drWindowOptions={a.value:a.name for a in WindowOptions}


class WindowEventType(enum.IntEnum):
    IMAQ_NO_EVENT                    =_int32(0)
    IMAQ_CLICK_EVENT                 =_int32(1)
    IMAQ_DRAW_EVENT                  =_int32(2)
    IMAQ_MOVE_EVENT                  =_int32(3)
    IMAQ_SIZE_EVENT                  =_int32(4)
    IMAQ_SCROLL_EVENT                =_int32(5)
    IMAQ_ACTIVATE_EVENT              =_int32(6)
    IMAQ_CLOSE_EVENT                 =_int32(7)
    IMAQ_DOUBLE_CLICK_EVENT          =_int32(8)
    IMAQ_WINDOW_EVENT_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dWindowEventType={a.name:a.value for a in WindowEventType}
drWindowEventType={a.value:a.name for a in WindowEventType}


class VisionInfoType(enum.IntEnum):
    IMAQ_ANY_VISION_INFO            =_int32(0)
    IMAQ_PATTERN_MATCHING_INFO      =_int32(1)
    IMAQ_CALIBRATION_INFO           =_int32(2)
    IMAQ_OVERLAY_INFO               =_int32(3)
    IMAQ_VISION_INFO_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dVisionInfoType={a.name:a.value for a in VisionInfoType}
drVisionInfoType={a.value:a.name for a in VisionInfoType}


class VerticalTextAlignment(enum.IntEnum):
    IMAQ_BOTTOM                            =_int32(0)
    IMAQ_TOP                               =_int32(1)
    IMAQ_BASELINE                          =_int32(2)
    IMAQ_VERTICAL_TEXT_ALIGNMENT_SIZE_GUARD=_int32(0xFFFFFFFF)
dVerticalTextAlignment={a.name:a.value for a in VerticalTextAlignment}
drVerticalTextAlignment={a.value:a.name for a in VerticalTextAlignment}


class ScalingMode(enum.IntEnum):
    IMAQ_SCALE_LARGER           =_int32(0)
    IMAQ_SCALE_SMALLER          =_int32(1)
    IMAQ_SCALING_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dScalingMode={a.name:a.value for a in ScalingMode}
drScalingMode={a.value:a.name for a in ScalingMode}


class TruncateMode(enum.IntEnum):
    IMAQ_TRUNCATE_LOW            =_int32(0)
    IMAQ_TRUNCATE_HIGH           =_int32(1)
    IMAQ_TRUNCATE_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dTruncateMode={a.name:a.value for a in TruncateMode}
drTruncateMode={a.value:a.name for a in TruncateMode}


class OutlineMethod(enum.IntEnum):
    IMAQ_EDGE_DIFFERENCE          =_int32(0)
    IMAQ_EDGE_GRADIENT            =_int32(1)
    IMAQ_EDGE_PREWITT             =_int32(2)
    IMAQ_EDGE_ROBERTS             =_int32(3)
    IMAQ_EDGE_SIGMA               =_int32(4)
    IMAQ_EDGE_SOBEL               =_int32(5)
    IMAQ_OUTLINE_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dOutlineMethod={a.name:a.value for a in OutlineMethod}
drOutlineMethod={a.value:a.name for a in OutlineMethod}


class TIFFCompressionType(enum.IntEnum):
    IMAQ_NO_COMPRESSION                  =_int32(0)
    IMAQ_JPEG                            =_int32(1)
    IMAQ_RUN_LENGTH                      =_int32(2)
    IMAQ_ZIP                             =_int32(3)
    IMAQ_TIFF_COMPRESSION_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dTIFFCompressionType={a.name:a.value for a in TIFFCompressionType}
drTIFFCompressionType={a.value:a.name for a in TIFFCompressionType}


class ThresholdMethod(enum.IntEnum):
    IMAQ_THRESH_CLUSTERING          =_int32(0)
    IMAQ_THRESH_ENTROPY             =_int32(1)
    IMAQ_THRESH_METRIC              =_int32(2)
    IMAQ_THRESH_MOMENTS             =_int32(3)
    IMAQ_THRESH_INTERCLASS          =_int32(4)
    IMAQ_THRESHOLD_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dThresholdMethod={a.name:a.value for a in ThresholdMethod}
drThresholdMethod={a.value:a.name for a in ThresholdMethod}


class TextAlignment(enum.IntEnum):
    IMAQ_LEFT                     =_int32(0)
    IMAQ_CENTER                   =_int32(1)
    IMAQ_RIGHT                    =_int32(2)
    IMAQ_TEXT_ALIGNMENT_SIZE_GUARD=_int32(0xFFFFFFFF)
dTextAlignment={a.name:a.value for a in TextAlignment}
drTextAlignment={a.value:a.name for a in TextAlignment}


class SpokeDirection(enum.IntEnum):
    IMAQ_OUTSIDE_TO_INSIDE         =_int32(0)
    IMAQ_INSIDE_TO_OUTSIDE         =_int32(1)
    IMAQ_SPOKE_DIRECTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dSpokeDirection={a.name:a.value for a in SpokeDirection}
drSpokeDirection={a.value:a.name for a in SpokeDirection}


class SkeletonMethod(enum.IntEnum):
    IMAQ_SKELETON_L                =_int32(0)
    IMAQ_SKELETON_M                =_int32(1)
    IMAQ_SKELETON_INVERSE          =_int32(2)
    IMAQ_SKELETON_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dSkeletonMethod={a.name:a.value for a in SkeletonMethod}
drSkeletonMethod={a.value:a.name for a in SkeletonMethod}


class SizeType(enum.IntEnum):
    IMAQ_KEEP_LARGE          =_int32(0)
    IMAQ_KEEP_SMALL          =_int32(1)
    IMAQ_SIZE_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dSizeType={a.name:a.value for a in SizeType}
drSizeType={a.value:a.name for a in SizeType}


class TwoEdgePolarityType(enum.IntEnum):
    IMAQ_NONE                             =_int32(0)
    IMAQ_RISING_FALLING                   =_int32(1)
    IMAQ_FALLING_RISING                   =_int32(2)
    IMAQ_RISING_RISING                    =_int32(3)
    IMAQ_FALLING_FALLING                  =_int32(4)
    IMAQ_TWO_EDGE_POLARITY_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dTwoEdgePolarityType={a.name:a.value for a in TwoEdgePolarityType}
drTwoEdgePolarityType={a.value:a.name for a in TwoEdgePolarityType}


class CalibrationROI(enum.IntEnum):
    IMAQ_FULL_IMAGE                =_int32(0)
    IMAQ_CALIBRATION_ROI           =_int32(1)
    IMAQ_USER_ROI                  =_int32(2)
    IMAQ_CALIBRATION_AND_USER_ROI  =_int32(3)
    IMAQ_CALIBRATION_OR_USER_ROI   =_int32(4)
    IMAQ_CALIBRATION_ROI_SIZE_GUARD=_int32(0xFFFFFFFF)
dCalibrationROI={a.name:a.value for a in CalibrationROI}
drCalibrationROI={a.value:a.name for a in CalibrationROI}


class ConcentricRakeDirection(enum.IntEnum):
    IMAQ_COUNTER_CLOCKWISE                   =_int32(0)
    IMAQ_CLOCKWISE                           =_int32(1)
    IMAQ_CONCENTRIC_RAKE_DIRECTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dConcentricRakeDirection={a.name:a.value for a in ConcentricRakeDirection}
drConcentricRakeDirection={a.value:a.name for a in ConcentricRakeDirection}


class ComplexPlane(enum.IntEnum):
    IMAQ_REAL                    =_int32(0)
    IMAQ_IMAGINARY               =_int32(1)
    IMAQ_MAGNITUDE               =_int32(2)
    IMAQ_PHASE                   =_int32(3)
    IMAQ_COMPLEX_PLANE_SIZE_GUARD=_int32(0xFFFFFFFF)
dComplexPlane={a.name:a.value for a in ComplexPlane}
drComplexPlane={a.value:a.name for a in ComplexPlane}


class MathTransformMethod(enum.IntEnum):
    IMAQ_TRANSFORM_LINEAR                =_int32(0)
    IMAQ_TRANSFORM_LOG                   =_int32(1)
    IMAQ_TRANSFORM_EXP                   =_int32(2)
    IMAQ_TRANSFORM_SQR                   =_int32(3)
    IMAQ_TRANSFORM_SQRT                  =_int32(4)
    IMAQ_TRANSFORM_POWX                  =_int32(5)
    IMAQ_TRANSFORM_POW1X                 =_int32(6)
    IMAQ_MATH_TRANSFORM_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dMathTransformMethod={a.name:a.value for a in MathTransformMethod}
drMathTransformMethod={a.value:a.name for a in MathTransformMethod}


class ColorSensitivity(enum.IntEnum):
    IMAQ_SENSITIVITY_LOW             =_int32(0)
    IMAQ_SENSITIVITY_MED             =_int32(1)
    IMAQ_SENSITIVITY_HIGH            =_int32(2)
    IMAQ_COLOR_SENSITIVITY_SIZE_GUARD=_int32(0xFFFFFFFF)
dColorSensitivity={a.name:a.value for a in ColorSensitivity}
drColorSensitivity={a.value:a.name for a in ColorSensitivity}


class ParticleInfoMode(enum.IntEnum):
    IMAQ_BASIC_INFO                   =_int32(0)
    IMAQ_ALL_INFO                     =_int32(1)
    IMAQ_PARTICLE_INFO_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dParticleInfoMode={a.name:a.value for a in ParticleInfoMode}
drParticleInfoMode={a.value:a.name for a in ParticleInfoMode}


class ContourType(enum.IntEnum):
    IMAQ_EMPTY_CONTOUR          =_int32(0)
    IMAQ_POINT                  =_int32(1)
    IMAQ_LINE                   =_int32(2)
    IMAQ_RECT                   =_int32(3)
    IMAQ_OVAL                   =_int32(4)
    IMAQ_CLOSED_CONTOUR         =_int32(5)
    IMAQ_OPEN_CONTOUR           =_int32(6)
    IMAQ_ANNULUS                =_int32(7)
    IMAQ_ROTATED_RECT           =_int32(8)
    IMAQ_CONTOUR_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dContourType={a.name:a.value for a in ContourType}
drContourType={a.value:a.name for a in ContourType}


class CalibrationUnit(enum.IntEnum):
    IMAQ_UNDEFINED                  =_int32(0)
    IMAQ_ANGSTROM                   =_int32(1)
    IMAQ_MICROMETER                 =_int32(2)
    IMAQ_MILLIMETER                 =_int32(3)
    IMAQ_CENTIMETER                 =_int32(4)
    IMAQ_METER                      =_int32(5)
    IMAQ_KILOMETER                  =_int32(6)
    IMAQ_MICROINCH                  =_int32(7)
    IMAQ_INCH                       =_int32(8)
    IMAQ_FOOT                       =_int32(9)
    IMAQ_NAUTICMILE                 =_int32(10)
    IMAQ_GROUNDMILE                 =_int32(11)
    IMAQ_STEP                       =_int32(12)
    IMAQ_CALIBRATION_UNIT_SIZE_GUARD=_int32(0xFFFFFFFF)
dCalibrationUnit={a.name:a.value for a in CalibrationUnit}
drCalibrationUnit={a.value:a.name for a in CalibrationUnit}


class ComparisonFunction(enum.IntEnum):
    IMAQ_CLEAR_LESS                 =_int32(0)
    IMAQ_CLEAR_LESS_OR_EQUAL        =_int32(1)
    IMAQ_CLEAR_EQUAL                =_int32(2)
    IMAQ_CLEAR_GREATER_OR_EQUAL     =_int32(3)
    IMAQ_CLEAR_GREATER              =_int32(4)
    IMAQ_COMPARE_FUNCTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dComparisonFunction={a.name:a.value for a in ComparisonFunction}
drComparisonFunction={a.value:a.name for a in ComparisonFunction}


class CalibrationMode(enum.IntEnum):
    IMAQ_PERSPECTIVE                =_int32(0)
    IMAQ_NONLINEAR                  =_int32(1)
    IMAQ_SIMPLE_CALIBRATION         =_int32(2)
    IMAQ_CORRECTED_IMAGE            =_int32(3)
    IMAQ_CALIBRATION_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dCalibrationMode={a.name:a.value for a in CalibrationMode}
drCalibrationMode={a.value:a.name for a in CalibrationMode}


class BrowserLocation(enum.IntEnum):
    IMAQ_INSERT_FIRST_FREE          =_int32(0)
    IMAQ_INSERT_END                 =_int32(1)
    IMAQ_BROWSER_LOCATION_SIZE_GUARD=_int32(0xFFFFFFFF)
dBrowserLocation={a.name:a.value for a in BrowserLocation}
drBrowserLocation={a.value:a.name for a in BrowserLocation}


class BrowserFrameStyle(enum.IntEnum):
    IMAQ_RAISED_FRAME                  =_int32(0)
    IMAQ_BEVELLED_FRAME                =_int32(1)
    IMAQ_OUTLINE_FRAME                 =_int32(2)
    IMAQ_HIDDEN_FRAME                  =_int32(3)
    IMAQ_STEP_FRAME                    =_int32(4)
    IMAQ_RAISED_OUTLINE_FRAME          =_int32(5)
    IMAQ_BROWSER_FRAME_STYLE_SIZE_GUARD=_int32(0xFFFFFFFF)
dBrowserFrameStyle={a.name:a.value for a in BrowserFrameStyle}
drBrowserFrameStyle={a.value:a.name for a in BrowserFrameStyle}


class BorderMethod(enum.IntEnum):
    IMAQ_BORDER_MIRROR           =_int32(0)
    IMAQ_BORDER_COPY             =_int32(1)
    IMAQ_BORDER_CLEAR            =_int32(2)
    IMAQ_BORDER_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dBorderMethod={a.name:a.value for a in BorderMethod}
drBorderMethod={a.value:a.name for a in BorderMethod}


class BarcodeType(enum.IntEnum):
    IMAQ_INVALID                =_int32((-1))
    IMAQ_CODABAR                =_int32(1)
    IMAQ_CODE39                 =_int32(2)
    IMAQ_CODE93                 =_int32(4)
    IMAQ_CODE128                =_int32(8)
    IMAQ_EAN8                   =_int32(16)
    IMAQ_EAN13                  =_int32(32)
    IMAQ_I2_OF_5                =_int32(64)
    IMAQ_MSI                    =_int32(128)
    IMAQ_UPCA                   =_int32(256)
    IMAQ_PHARMACODE             =_int32(512)
    IMAQ_RSS_LIMITED            =_int32(1024)
    IMAQ_BARCODE_TYPE_SIZE_GUARD=_int32(0x7FFFFFFF)
dBarcodeType={a.name:a.value for a in BarcodeType}
drBarcodeType={a.value:a.name for a in BarcodeType}


class AxisOrientation(enum.IntEnum):
    IMAQ_DIRECT                     =_int32(0)
    IMAQ_INDIRECT                   =_int32(1)
    IMAQ_AXIS_ORIENTATION_SIZE_GUARD=_int32(0xFFFFFFFF)
dAxisOrientation={a.name:a.value for a in AxisOrientation}
drAxisOrientation={a.value:a.name for a in AxisOrientation}


class ColorIgnoreMode(enum.IntEnum):
    IMAQ_IGNORE_NONE                       =_int32(0)
    IMAQ_IGNORE_BLACK                      =_int32(1)
    IMAQ_IGNORE_WHITE                      =_int32(2)
    IMAQ_IGNORE_BLACK_AND_WHITE            =_int32(3)
    IMAQ_BLACK_WHITE_IGNORE_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dColorIgnoreMode={a.name:a.value for a in ColorIgnoreMode}
drColorIgnoreMode={a.value:a.name for a in ColorIgnoreMode}


class LineGaugeMethod(enum.IntEnum):
    IMAQ_EDGE_TO_EDGE                =_int32(0)
    IMAQ_EDGE_TO_POINT               =_int32(1)
    IMAQ_POINT_TO_EDGE               =_int32(2)
    IMAQ_POINT_TO_POINT              =_int32(3)
    IMAQ_LINE_GAUGE_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dLineGaugeMethod={a.name:a.value for a in LineGaugeMethod}
drLineGaugeMethod={a.value:a.name for a in LineGaugeMethod}


class MatchingMode(enum.IntEnum):
    IMAQ_MATCH_SHIFT_INVARIANT   =_int32(1)
    IMAQ_MATCH_ROTATION_INVARIANT=_int32(2)
    IMAQ_MATCHING_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dMatchingMode={a.name:a.value for a in MatchingMode}
drMatchingMode={a.value:a.name for a in MatchingMode}


class MatchingAlgorithm(enum.IntEnum):
    IMAQ_MATCH_ALLALGORITHMS          =_int32(0)
    IMAQ_MATCH_LOW_DISCREPANCY        =_int32(1)
    IMAQ_MATCH_GRAYVALUE_PYRAMID      =_int32(2)
    IMAQ_MATCH_GRADIENT_PYRAMID       =_int32(3)
    IMAQ_MATCHING_ALGORITHM_SIZE_GUARD=_int32(0xFFFFFFFF)
dMatchingAlgorithm={a.name:a.value for a in MatchingAlgorithm}
drMatchingAlgorithm={a.value:a.name for a in MatchingAlgorithm}


class PatternMatchPresetFunction(enum.IntEnum):
    IMAQ_SET_DEFAULT_OPTIONS       =_int32(1)
    IMAQ_SET_PRESET_OPTIONS        =_int32(2)
    IMAQ_PRESET_FUNCTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dPatternMatchPresetFunction={a.name:a.value for a in PatternMatchPresetFunction}
drPatternMatchPresetFunction={a.value:a.name for a in PatternMatchPresetFunction}


class PatternMatchPresetType(enum.IntEnum):
    IMAQ_PRESET_USE_CASE       =_int32(0)
    IMAQ_PRESET_PRIORITY       =_int32(1)
    IMAQ_PRESET_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dPatternMatchPresetType={a.name:a.value for a in PatternMatchPresetType}
drPatternMatchPresetType={a.value:a.name for a in PatternMatchPresetType}


class ColorMode(enum.IntEnum):
    IMAQ_RGB                  =_int32(0)
    IMAQ_HSL                  =_int32(1)
    IMAQ_HSV                  =_int32(2)
    IMAQ_HSI                  =_int32(3)
    IMAQ_CIE                  =_int32(4)
    IMAQ_CIEXYZ               =_int32(5)
    IMAQ_COLOR_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dColorMode={a.name:a.value for a in ColorMode}
drColorMode={a.value:a.name for a in ColorMode}


class MappingMethod(enum.IntEnum):
    IMAQ_FULL_DYNAMIC             =_int32(0)
    IMAQ_DOWNSHIFT                =_int32(1)
    IMAQ_RANGE                    =_int32(2)
    IMAQ_90_PCT_DYNAMIC           =_int32(3)
    IMAQ_PERCENT_RANGE            =_int32(4)
    IMAQ_DEFAULT_MAPPING          =_int32(10)
    IMAQ_MOST_SIGNIFICANT         =_int32(11)
    IMAQ_FULL_DYNAMIC_ALWAYS      =_int32(12)
    IMAQ_DOWNSHIFT_ALWAYS         =_int32(13)
    IMAQ_RANGE_ALWAYS             =_int32(14)
    IMAQ_90_PCT_DYNAMIC_ALWAYS    =_int32(15)
    IMAQ_PERCENT_RANGE_ALWAYS     =_int32(16)
    IMAQ_MAPPING_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dMappingMethod={a.name:a.value for a in MappingMethod}
drMappingMethod={a.value:a.name for a in MappingMethod}


class DetectionMode(enum.IntEnum):
    IMAQ_DETECT_PEAKS             =_int32(0)
    IMAQ_DETECT_VALLEYS           =_int32(1)
    IMAQ_DETECTION_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dDetectionMode={a.name:a.value for a in DetectionMode}
drDetectionMode={a.value:a.name for a in DetectionMode}


class LevelType(enum.IntEnum):
    IMAQ_ABSOLUTE             =_int32(0)
    IMAQ_RELATIVE             =_int32(1)
    IMAQ_LEVEL_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dLevelType={a.name:a.value for a in LevelType}
drLevelType={a.value:a.name for a in LevelType}


class LearningMode(enum.IntEnum):
    IMAQ_LEARN_ALL                 =_int32(0)
    IMAQ_LEARN_SHIFT_INFORMATION   =_int32(1)
    IMAQ_LEARN_ROTATION_INFORMATION=_int32(2)
    IMAQ_LEARNING_MODE_SIZE_GUARD  =_int32(0xFFFFFFFF)
dLearningMode={a.name:a.value for a in LearningMode}
drLearningMode={a.value:a.name for a in LearningMode}


class KernelFamily(enum.IntEnum):
    IMAQ_GRADIENT_FAMILY         =_int32(0)
    IMAQ_LAPLACIAN_FAMILY        =_int32(1)
    IMAQ_SMOOTHING_FAMILY        =_int32(2)
    IMAQ_GAUSSIAN_FAMILY         =_int32(3)
    IMAQ_KERNEL_FAMILY_SIZE_GUARD=_int32(0xFFFFFFFF)
dKernelFamily={a.name:a.value for a in KernelFamily}
drKernelFamily={a.value:a.name for a in KernelFamily}


class ImageType(enum.IntEnum):
    IMAQ_IMAGE_U8             =_int32(0)
    IMAQ_IMAGE_U16            =_int32(7)
    IMAQ_IMAGE_I16            =_int32(1)
    IMAQ_IMAGE_SGL            =_int32(2)
    IMAQ_IMAGE_COMPLEX        =_int32(3)
    IMAQ_IMAGE_RGB            =_int32(4)
    IMAQ_IMAGE_HSL            =_int32(5)
    IMAQ_IMAGE_RGB_U64        =_int32(6)
    IMAQ_IMAGE_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dImageType={a.name:a.value for a in ImageType}
drImageType={a.value:a.name for a in ImageType}


class CastingMethod(enum.IntEnum):
    IMAQ_USE_BIT_DEPTH            =_int32(0)
    IMAQ_USE_SHIFT                =_int32(1)
    IMAQ_USE_LOOKUP_TABLE         =_int32(2)
    IMAQ_CASTING_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dCastingMethod={a.name:a.value for a in CastingMethod}
drCastingMethod={a.value:a.name for a in CastingMethod}


class ImageFeatureMode(enum.IntEnum):
    IMAQ_COLOR_AND_SHAPE_FEATURES=_int32(0)
    IMAQ_COLOR_FEATURES          =_int32(1)
    IMAQ_SHAPE_FEATURES          =_int32(2)
    IMAQ_FEATURE_MODE_SIZE_GUARD =_int32(0xFFFFFFFF)
dImageFeatureMode={a.name:a.value for a in ImageFeatureMode}
drImageFeatureMode={a.value:a.name for a in ImageFeatureMode}


class FontColor(enum.IntEnum):
    IMAQ_WHITE                =_int32(0)
    IMAQ_BLACK                =_int32(1)
    IMAQ_INVERT               =_int32(2)
    IMAQ_BLACK_ON_WHITE       =_int32(3)
    IMAQ_WHITE_ON_BLACK       =_int32(4)
    IMAQ_FONT_COLOR_SIZE_GUARD=_int32(0xFFFFFFFF)
dFontColor={a.name:a.value for a in FontColor}
drFontColor={a.value:a.name for a in FontColor}


class FlipAxis(enum.IntEnum):
    IMAQ_HORIZONTAL_AXIS     =_int32(0)
    IMAQ_VERTICAL_AXIS       =_int32(1)
    IMAQ_CENTER_AXIS         =_int32(2)
    IMAQ_DIAG_L_TO_R_AXIS    =_int32(3)
    IMAQ_DIAG_R_TO_L_AXIS    =_int32(4)
    IMAQ_FLIP_AXIS_SIZE_GUARD=_int32(0xFFFFFFFF)
dFlipAxis={a.name:a.value for a in FlipAxis}
drFlipAxis={a.value:a.name for a in FlipAxis}


class EdgeProcess(enum.IntEnum):
    IMAQ_FIRST                  =_int32(0)
    IMAQ_FIRST_AND_LAST         =_int32(1)
    IMAQ_ALL                    =_int32(2)
    IMAQ_BEST                   =_int32(3)
    IMAQ_EDGE_PROCESS_SIZE_GUARD=_int32(0xFFFFFFFF)
dEdgeProcess={a.name:a.value for a in EdgeProcess}
drEdgeProcess={a.value:a.name for a in EdgeProcess}


class DrawMode(enum.IntEnum):
    IMAQ_DRAW_VALUE          =_int32(0)
    IMAQ_DRAW_INVERT         =_int32(2)
    IMAQ_PAINT_VALUE         =_int32(1)
    IMAQ_PAINT_INVERT        =_int32(3)
    IMAQ_HIGHLIGHT_VALUE     =_int32(4)
    IMAQ_DRAW_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dDrawMode={a.name:a.value for a in DrawMode}
drDrawMode={a.value:a.name for a in DrawMode}


class Direction3D(enum.IntEnum):
    IMAQ_3D_NW                  =_int32(0)
    IMAQ_3D_SW                  =_int32(1)
    IMAQ_3D_SE                  =_int32(2)
    IMAQ_3D_NE                  =_int32(3)
    IMAQ_DIRECTION_3D_SIZE_GUARD=_int32(0xFFFFFFFF)
dDirection3D={a.name:a.value for a in Direction3D}
drDirection3D={a.value:a.name for a in Direction3D}


class InterpolationMethod(enum.IntEnum):
    IMAQ_ZERO_ORDER                     =_int32(0)
    IMAQ_BILINEAR                       =_int32(1)
    IMAQ_QUADRATIC                      =_int32(2)
    IMAQ_CUBIC_SPLINE                   =_int32(3)
    IMAQ_BILINEAR_FIXED                 =_int32(4)
    IMAQ_INTERPOLATION_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dInterpolationMethod={a.name:a.value for a in InterpolationMethod}
drInterpolationMethod={a.value:a.name for a in InterpolationMethod}


class ReadResolution(enum.IntEnum):
    IMAQ_LOW_RESOLUTION            =_int32(0)
    IMAQ_MEDIUM_RESOLUTION         =_int32(1)
    IMAQ_HIGH_RESOLUTION           =_int32(2)
    IMAQ_READ_RESOLUTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dReadResolution={a.name:a.value for a in ReadResolution}
drReadResolution={a.value:a.name for a in ReadResolution}


class WriteClassifierFileMode(enum.IntEnum):
    IMAQ_CLASSIFIER_WRITE_ALL                  =_int32(0)
    IMAQ_CLASSIFIER_WRITE_CLASSIFY_ONLY        =_int32(1)
    IMAQ_WRITE_CLASSIFIER_FILE_MODES_SIZE_GUARD=_int32(0xFFFFFFFF)
dWriteClassifierFileMode={a.name:a.value for a in WriteClassifierFileMode}
drWriteClassifierFileMode={a.value:a.name for a in WriteClassifierFileMode}


class NearestNeighborMetric(enum.IntEnum):
    IMAQ_METRIC_MAXIMUM                    =_int32(0)
    IMAQ_METRIC_SUM                        =_int32(1)
    IMAQ_METRIC_EUCLIDEAN                  =_int32(2)
    IMAQ_NEAREST_NEIGHBOR_METRIC_SIZE_GUARD=_int32(0xFFFFFFFF)
dNearestNeighborMetric={a.name:a.value for a in NearestNeighborMetric}
drNearestNeighborMetric={a.value:a.name for a in NearestNeighborMetric}


class NearestNeighborMethod(enum.IntEnum):
    IMAQ_MINIMUM_MEAN_DISTANCE             =_int32(0)
    IMAQ_K_NEAREST_NEIGHBOR                =_int32(1)
    IMAQ_NEAREST_PROTOTYPE                 =_int32(2)
    IMAQ_NEAREST_NEIGHBOR_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dNearestNeighborMethod={a.name:a.value for a in NearestNeighborMethod}
drNearestNeighborMethod={a.value:a.name for a in NearestNeighborMethod}


class ParticleClassifierType(enum.IntEnum):
    IMAQ_PARTICLE_LARGEST                   =_int32(0)
    IMAQ_PARTICLE_ALL                       =_int32(1)
    IMAQ_PARTICLE_CLASSIFIER_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dParticleClassifierType={a.name:a.value for a in ParticleClassifierType}
drParticleClassifierType={a.value:a.name for a in ParticleClassifierType}


class ButtonLabel(enum.IntEnum):
    IMAQ_BUTTON_OK              =_int32(0)
    IMAQ_BUTTON_SAVE            =_int32(1)
    IMAQ_BUTTON_SELECT          =_int32(2)
    IMAQ_BUTTON_LOAD            =_int32(3)
    IMAQ_BUTTON_LABEL_SIZE_GUARD=_int32(0xFFFFFFFF)
dButtonLabel={a.name:a.value for a in ButtonLabel}
drButtonLabel={a.value:a.name for a in ButtonLabel}


class GeometricMatchingMode(enum.IntEnum):
    IMAQ_GEOMETRIC_MATCH_SHIFT_INVARIANT    =_int32(0)
    IMAQ_GEOMETRIC_MATCH_ROTATION_INVARIANT =_int32(1)
    IMAQ_GEOMETRIC_MATCH_SCALE_INVARIANT    =_int32(2)
    IMAQ_GEOMETRIC_MATCH_OCCLUSION_INVARIANT=_int32(4)
    IMAQ_GEOMETRIC_MATCHING_MODE_SIZE_GUARD =_int32(0xFFFFFFFF)
dGeometricMatchingMode={a.name:a.value for a in GeometricMatchingMode}
drGeometricMatchingMode={a.value:a.name for a in GeometricMatchingMode}


class MeasurementType(enum.IntEnum):
    IMAQ_MT_CENTER_OF_MASS_X                   =_int32(0)
    IMAQ_MT_CENTER_OF_MASS_Y                   =_int32(1)
    IMAQ_MT_FIRST_PIXEL_X                      =_int32(2)
    IMAQ_MT_FIRST_PIXEL_Y                      =_int32(3)
    IMAQ_MT_BOUNDING_RECT_LEFT                 =_int32(4)
    IMAQ_MT_BOUNDING_RECT_TOP                  =_int32(5)
    IMAQ_MT_BOUNDING_RECT_RIGHT                =_int32(6)
    IMAQ_MT_BOUNDING_RECT_BOTTOM               =_int32(7)
    IMAQ_MT_MAX_FERET_DIAMETER_START_X         =_int32(8)
    IMAQ_MT_MAX_FERET_DIAMETER_START_Y         =_int32(9)
    IMAQ_MT_MAX_FERET_DIAMETER_END_X           =_int32(10)
    IMAQ_MT_MAX_FERET_DIAMETER_END_Y           =_int32(11)
    IMAQ_MT_MAX_HORIZ_SEGMENT_LENGTH_LEFT      =_int32(12)
    IMAQ_MT_MAX_HORIZ_SEGMENT_LENGTH_RIGHT     =_int32(13)
    IMAQ_MT_MAX_HORIZ_SEGMENT_LENGTH_ROW       =_int32(14)
    IMAQ_MT_BOUNDING_RECT_WIDTH                =_int32(16)
    IMAQ_MT_BOUNDING_RECT_HEIGHT               =_int32(17)
    IMAQ_MT_BOUNDING_RECT_DIAGONAL             =_int32(18)
    IMAQ_MT_PERIMETER                          =_int32(19)
    IMAQ_MT_CONVEX_HULL_PERIMETER              =_int32(20)
    IMAQ_MT_HOLES_PERIMETER                    =_int32(21)
    IMAQ_MT_MAX_FERET_DIAMETER                 =_int32(22)
    IMAQ_MT_EQUIVALENT_ELLIPSE_MAJOR_AXIS      =_int32(23)
    IMAQ_MT_EQUIVALENT_ELLIPSE_MINOR_AXIS      =_int32(24)
    IMAQ_MT_EQUIVALENT_ELLIPSE_MINOR_AXIS_FERET=_int32(25)
    IMAQ_MT_EQUIVALENT_RECT_LONG_SIDE          =_int32(26)
    IMAQ_MT_EQUIVALENT_RECT_SHORT_SIDE         =_int32(27)
    IMAQ_MT_EQUIVALENT_RECT_DIAGONAL           =_int32(28)
    IMAQ_MT_EQUIVALENT_RECT_SHORT_SIDE_FERET   =_int32(29)
    IMAQ_MT_AVERAGE_HORIZ_SEGMENT_LENGTH       =_int32(30)
    IMAQ_MT_AVERAGE_VERT_SEGMENT_LENGTH        =_int32(31)
    IMAQ_MT_HYDRAULIC_RADIUS                   =_int32(32)
    IMAQ_MT_WADDEL_DISK_DIAMETER               =_int32(33)
    IMAQ_MT_AREA                               =_int32(35)
    IMAQ_MT_HOLES_AREA                         =_int32(36)
    IMAQ_MT_PARTICLE_AND_HOLES_AREA            =_int32(37)
    IMAQ_MT_CONVEX_HULL_AREA                   =_int32(38)
    IMAQ_MT_IMAGE_AREA                         =_int32(39)
    IMAQ_MT_NUMBER_OF_HOLES                    =_int32(41)
    IMAQ_MT_NUMBER_OF_HORIZ_SEGMENTS           =_int32(42)
    IMAQ_MT_NUMBER_OF_VERT_SEGMENTS            =_int32(43)
    IMAQ_MT_ORIENTATION                        =_int32(45)
    IMAQ_MT_MAX_FERET_DIAMETER_ORIENTATION     =_int32(46)
    IMAQ_MT_AREA_BY_IMAGE_AREA                 =_int32(48)
    IMAQ_MT_AREA_BY_PARTICLE_AND_HOLES_AREA    =_int32(49)
    IMAQ_MT_RATIO_OF_EQUIVALENT_ELLIPSE_AXES   =_int32(50)
    IMAQ_MT_RATIO_OF_EQUIVALENT_RECT_SIDES     =_int32(51)
    IMAQ_MT_ELONGATION_FACTOR                  =_int32(53)
    IMAQ_MT_COMPACTNESS_FACTOR                 =_int32(54)
    IMAQ_MT_HEYWOOD_CIRCULARITY_FACTOR         =_int32(55)
    IMAQ_MT_TYPE_FACTOR                        =_int32(56)
    IMAQ_MT_SUM_X                              =_int32(58)
    IMAQ_MT_SUM_Y                              =_int32(59)
    IMAQ_MT_SUM_XX                             =_int32(60)
    IMAQ_MT_SUM_XY                             =_int32(61)
    IMAQ_MT_SUM_YY                             =_int32(62)
    IMAQ_MT_SUM_XXX                            =_int32(63)
    IMAQ_MT_SUM_XXY                            =_int32(64)
    IMAQ_MT_SUM_XYY                            =_int32(65)
    IMAQ_MT_SUM_YYY                            =_int32(66)
    IMAQ_MT_MOMENT_OF_INERTIA_XX               =_int32(68)
    IMAQ_MT_MOMENT_OF_INERTIA_XY               =_int32(69)
    IMAQ_MT_MOMENT_OF_INERTIA_YY               =_int32(70)
    IMAQ_MT_MOMENT_OF_INERTIA_XXX              =_int32(71)
    IMAQ_MT_MOMENT_OF_INERTIA_XXY              =_int32(72)
    IMAQ_MT_MOMENT_OF_INERTIA_XYY              =_int32(73)
    IMAQ_MT_MOMENT_OF_INERTIA_YYY              =_int32(74)
    IMAQ_MT_NORM_MOMENT_OF_INERTIA_XX          =_int32(75)
    IMAQ_MT_NORM_MOMENT_OF_INERTIA_XY          =_int32(76)
    IMAQ_MT_NORM_MOMENT_OF_INERTIA_YY          =_int32(77)
    IMAQ_MT_NORM_MOMENT_OF_INERTIA_XXX         =_int32(78)
    IMAQ_MT_NORM_MOMENT_OF_INERTIA_XXY         =_int32(79)
    IMAQ_MT_NORM_MOMENT_OF_INERTIA_XYY         =_int32(80)
    IMAQ_MT_NORM_MOMENT_OF_INERTIA_YYY         =_int32(81)
    IMAQ_MT_HU_MOMENT_1                        =_int32(82)
    IMAQ_MT_HU_MOMENT_2                        =_int32(83)
    IMAQ_MT_HU_MOMENT_3                        =_int32(84)
    IMAQ_MT_HU_MOMENT_4                        =_int32(85)
    IMAQ_MT_HU_MOMENT_5                        =_int32(86)
    IMAQ_MT_HU_MOMENT_6                        =_int32(87)
    IMAQ_MT_HU_MOMENT_7                        =_int32(88)
    IMAQ_MEASUREMENT_TYPE_SIZE_GUARD           =_int32(0xFFFFFFFF)
dMeasurementType={a.name:a.value for a in MeasurementType}
drMeasurementType={a.value:a.name for a in MeasurementType}


class ParticleType(enum.IntEnum):
    IMAQ_PARTICLE_BRIGHT         =_int32(0)
    IMAQ_PARTICLE_DARK           =_int32(1)
    IMAQ_PARTICLE_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dParticleType={a.name:a.value for a in ParticleType}
drParticleType={a.value:a.name for a in ParticleType}


class ThresholdMode(enum.IntEnum):
    IMAQ_FIXED_RANGE              =_int32(0)
    IMAQ_COMPUTED_UNIFORM         =_int32(1)
    IMAQ_COMPUTED_LINEAR          =_int32(2)
    IMAQ_COMPUTED_NONLINEAR       =_int32(3)
    IMAQ_THRESHOLD_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dThresholdMode={a.name:a.value for a in ThresholdMode}
drThresholdMode={a.value:a.name for a in ThresholdMode}


class ReadStrategy(enum.IntEnum):
    IMAQ_READ_AGGRESSIVE         =_int32(0)
    IMAQ_READ_CONSERVATIVE       =_int32(1)
    IMAQ_READ_STRATEGY_SIZE_GUARD=_int32(0xFFFFFFFF)
dReadStrategy={a.name:a.value for a in ReadStrategy}
drReadStrategy={a.value:a.name for a in ReadStrategy}


class GroupBehavior(enum.IntEnum):
    IMAQ_GROUP_CLEAR              =_int32(0)
    IMAQ_GROUP_KEEP               =_int32(1)
    IMAQ_GROUP_TRANSFORM          =_int32(2)
    IMAQ_GROUP_BEHAVIOR_SIZE_GUARD=_int32(0xFFFFFFFF)
dGroupBehavior={a.name:a.value for a in GroupBehavior}
drGroupBehavior={a.value:a.name for a in GroupBehavior}


class QRGradingMode(enum.IntEnum):
    IMAQ_QR_NO_GRADING             =_int32(0)
    IMAQ_QR_GRADING_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dQRGradingMode={a.name:a.value for a in QRGradingMode}
drQRGradingMode={a.value:a.name for a in QRGradingMode}


class MeasureParticlesCalibrationMode(enum.IntEnum):
    IMAQ_CALIBRATION_MODE_PIXEL                       =_int32(0)
    IMAQ_CALIBRATION_MODE_CALIBRATED                  =_int32(1)
    IMAQ_CALIBRATION_MODE_BOTH                        =_int32(2)
    IMAQ_MEASURE_PARTICLES_CALIBRATION_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dMeasureParticlesCalibrationMode={a.name:a.value for a in MeasureParticlesCalibrationMode}
drMeasureParticlesCalibrationMode={a.value:a.name for a in MeasureParticlesCalibrationMode}


class ThresholdType(enum.IntEnum):
    IMAQ_GLOBAL_THRESHOLD         =_int32(0)
    IMAQ_LOCAL_THRESHOLD          =_int32(1)
    IMAQ_COLOR_THRESHOLD          =_int32(2)
    IMAQ_THRESHOLD_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dThresholdType={a.name:a.value for a in ThresholdType}
drThresholdType={a.value:a.name for a in ThresholdType}


class LineSeparator(enum.IntEnum):
    IMAQ_END_OF_LINE_CONSTANT     =_int32(0)
    IMAQ_LINE_FEED                =_int32(1)
    IMAQ_CARRIAGE_RETURN          =_int32(2)
    IMAQ_LINE_SEPARATOR_SIZE_GUARD=_int32(0xFFFFFFFF)
dLineSeparator={a.name:a.value for a in LineSeparator}
drLineSeparator={a.value:a.name for a in LineSeparator}


class GeometricMatchingSearchStrategy(enum.IntEnum):
    IMAQ_GEOMETRIC_MATCHING_CONSERVATIVE              =_int32(0)
    IMAQ_GEOMETRIC_MATCHING_BALANCED                  =_int32(1)
    IMAQ_GEOMETRIC_MATCHING_AGGRESSIVE                =_int32(2)
    IMAQ_GEOMETRIC_MATCHING_SEARCH_STRATEGY_SIZE_GUARD=_int32(0xFFFFFFFF)
dGeometricMatchingSearchStrategy={a.name:a.value for a in GeometricMatchingSearchStrategy}
drGeometricMatchingSearchStrategy={a.value:a.name for a in GeometricMatchingSearchStrategy}


class ColorClassificationResolution(enum.IntEnum):
    IMAQ_CLASSIFIER_LOW_RESOLUTION       =_int32(0)
    IMAQ_CLASSIFIER_MEDIUM_RESOLUTION    =_int32(1)
    IMAQ_CLASSIFIER_HIGH_RESOLUTION      =_int32(2)
    IMAQ_CLASSIFIER_RESOLUTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dColorClassificationResolution={a.name:a.value for a in ColorClassificationResolution}
drColorClassificationResolution={a.value:a.name for a in ColorClassificationResolution}


class ContrastMode(enum.IntEnum):
    IMAQ_ORIGINAL_CONTRAST=_int32(0)
    IMAQ_REVERSED_CONTRAST=_int32(1)
    IMAQ_BOTH_CONTRASTS   =_int32(2)
dContrastMode={a.name:a.value for a in ContrastMode}
drContrastMode={a.value:a.name for a in ContrastMode}


class RoundingMode(enum.IntEnum):
    IMAQ_ROUNDING_MODE_OPTIMIZE  =_int32(0)
    IMAQ_ROUNDING_MODE_TRUNCATE  =_int32(1)
    IMAQ_ROUNDING_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dRoundingMode={a.name:a.value for a in RoundingMode}
drRoundingMode={a.value:a.name for a in RoundingMode}


class FindTransformMode(enum.IntEnum):
    IMAQ_FIND_REFERENCE                =_int32(0)
    IMAQ_UPDATE_TRANSFORM              =_int32(1)
    IMAQ_FIND_TRANSFORM_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dFindTransformMode={a.name:a.value for a in FindTransformMode}
drFindTransformMode={a.value:a.name for a in FindTransformMode}


class WaveletType(enum.IntEnum):
    IMAQ_DB02                =_int32(0)
    IMAQ_DB03                =_int32(1)
    IMAQ_DB04                =_int32(2)
    IMAQ_DB05                =_int32(3)
    IMAQ_DB06                =_int32(4)
    IMAQ_DB07                =_int32(5)
    IMAQ_DB08                =_int32(6)
    IMAQ_DB09                =_int32(7)
    IMAQ_DB10                =_int32(8)
    IMAQ_DB11                =_int32(9)
    IMAQ_DB12                =_int32(10)
    IMAQ_DB13                =_int32(11)
    IMAQ_DB14                =_int32(12)
    IMAQ_HAAR                =_int32(13)
    IMAQ_BIOR1_3             =_int32(14)
    IMAQ_BIOR1_5             =_int32(15)
    IMAQ_BIOR2_2             =_int32(16)
    IMAQ_BIOR2_4             =_int32(17)
    IMAQ_BIOR2_6             =_int32(18)
    IMAQ_BIOR2_8             =_int32(19)
    IMAQ_BIOR3_1             =_int32(20)
    IMAQ_BIOR3_3             =_int32(21)
    IMAQ_BIOR3_5             =_int32(22)
    IMAQ_BIOR3_7             =_int32(23)
    IMAQ_BIOR3_9             =_int32(24)
    IMAQ_BIOR4_4             =_int32(25)
    IMAQ_COIF1               =_int32(26)
    IMAQ_COIF2               =_int32(27)
    IMAQ_COIF3               =_int32(28)
    IMAQ_COIF4               =_int32(29)
    IMAQ_COIF5               =_int32(30)
    IMAQ_SYM2                =_int32(31)
    IMAQ_SYM3                =_int32(32)
    IMAQ_SYM4                =_int32(33)
    IMAQ_SYM5                =_int32(34)
    IMAQ_SYM6                =_int32(35)
    IMAQ_SYM7                =_int32(36)
    IMAQ_SYM8                =_int32(37)
    IMAQ_BIOR5_5             =_int32(38)
    IMAQ_BIOR6_8             =_int32(39)
    IMAQ_WAVE_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dWaveletType={a.name:a.value for a in WaveletType}
drWaveletType={a.value:a.name for a in WaveletType}


class MulticoreOperation(enum.IntEnum):
    IMAQ_GET_CORES                     =_int32(0)
    IMAQ_SET_CORES                     =_int32(1)
    IMAQ_USE_MAX_AVAILABLE             =_int32(2)
    IMAQ_MULTICORE_OPERATION_SIZE_GUARD=_int32(0xFFFFFFFF)
dMulticoreOperation={a.name:a.value for a in MulticoreOperation}
drMulticoreOperation={a.value:a.name for a in MulticoreOperation}


class MorphologyReconstructOperation(enum.IntEnum):
    IMAQ_DILATE_RECONSTRUCT                         =_int32(0)
    IMAQ_ERODE_RECONSTRUCT                          =_int32(1)
    IMAQ_MORPHOLOGY_RECONSTRUCT_OPERATION_SIZE_GUARD=_int32(0xFFFFFFFF)
dMorphologyReconstructOperation={a.name:a.value for a in MorphologyReconstructOperation}
drMorphologyReconstructOperation={a.value:a.name for a in MorphologyReconstructOperation}


class QRDimensions(enum.IntEnum):
    IMAQ_QR_DIMENSIONS_AUTO_DETECT=_int32(0)
    IMAQ_QR_DIMENSIONS_11x11      =_int32(11)
    IMAQ_QR_DIMENSIONS_13x13      =_int32(13)
    IMAQ_QR_DIMENSIONS_15x15      =_int32(15)
    IMAQ_QR_DIMENSIONS_17x17      =_int32(17)
    IMAQ_QR_DIMENSIONS_21x21      =_int32(21)
    IMAQ_QR_DIMENSIONS_25x25      =_int32(25)
    IMAQ_QR_DIMENSIONS_29x29      =_int32(29)
    IMAQ_QR_DIMENSIONS_33x33      =_int32(33)
    IMAQ_QR_DIMENSIONS_37x37      =_int32(37)
    IMAQ_QR_DIMENSIONS_41x41      =_int32(41)
    IMAQ_QR_DIMENSIONS_45x45      =_int32(45)
    IMAQ_QR_DIMENSIONS_49x49      =_int32(49)
    IMAQ_QR_DIMENSIONS_53x53      =_int32(53)
    IMAQ_QR_DIMENSIONS_57x57      =_int32(57)
    IMAQ_QR_DIMENSIONS_61x61      =_int32(61)
    IMAQ_QR_DIMENSIONS_65x65      =_int32(65)
    IMAQ_QR_DIMENSIONS_69x69      =_int32(69)
    IMAQ_QR_DIMENSIONS_73x73      =_int32(73)
    IMAQ_QR_DIMENSIONS_77x77      =_int32(77)
    IMAQ_QR_DIMENSIONS_81x81      =_int32(81)
    IMAQ_QR_DIMENSIONS_85x85      =_int32(85)
    IMAQ_QR_DIMENSIONS_89x89      =_int32(89)
    IMAQ_QR_DIMENSIONS_93x93      =_int32(93)
    IMAQ_QR_DIMENSIONS_97x97      =_int32(97)
    IMAQ_QR_DIMENSIONS_101x101    =_int32(101)
    IMAQ_QR_DIMENSIONS_105x105    =_int32(105)
    IMAQ_QR_DIMENSIONS_109x109    =_int32(109)
    IMAQ_QR_DIMENSIONS_113x113    =_int32(113)
    IMAQ_QR_DIMENSIONS_117x117    =_int32(117)
    IMAQ_QR_DIMENSIONS_121x121    =_int32(121)
    IMAQ_QR_DIMENSIONS_125x125    =_int32(125)
    IMAQ_QR_DIMENSIONS_129x129    =_int32(129)
    IMAQ_QR_DIMENSIONS_133x133    =_int32(133)
    IMAQ_QR_DIMENSIONS_137x137    =_int32(137)
    IMAQ_QR_DIMENSIONS_141x141    =_int32(141)
    IMAQ_QR_DIMENSIONS_145x145    =_int32(145)
    IMAQ_QR_DIMENSIONS_149x149    =_int32(149)
    IMAQ_QR_DIMENSIONS_153x153    =_int32(153)
    IMAQ_QR_DIMENSIONS_157x157    =_int32(157)
    IMAQ_QR_DIMENSIONS_161x161    =_int32(161)
    IMAQ_QR_DIMENSIONS_165x165    =_int32(165)
    IMAQ_QR_DIMENSIONS_169x169    =_int32(169)
    IMAQ_QR_DIMENSIONS_173x173    =_int32(173)
    IMAQ_QR_DIMENSIONS_177x177    =_int32(177)
    IMAQ_QR_DIMENSIONS_SIZE_GUARD =_int32(0xFFFFFFFF)
dQRDimensions={a.name:a.value for a in QRDimensions}
drQRDimensions={a.value:a.name for a in QRDimensions}


class QRCellFilterMode(enum.IntEnum):
    IMAQ_QR_CELL_FILTER_MODE_AUTO_DETECT      =_int32((-2))
    IMAQ_QR_CELL_FILTER_MODE_AVERAGE          =_int32(0)
    IMAQ_QR_CELL_FILTER_MODE_MEDIAN           =_int32(1)
    IMAQ_QR_CELL_FILTER_MODE_CENTRAL_AVERAGE  =_int32(2)
    IMAQ_QR_CELL_FILTER_MODE_HIGH_AVERAGE     =_int32(3)
    IMAQ_QR_CELL_FILTER_MODE_LOW_AVERAGE      =_int32(4)
    IMAQ_QR_CELL_FILTER_MODE_VERY_HIGH_AVERAGE=_int32(5)
    IMAQ_QR_CELL_FILTER_MODE_VERY_LOW_AVERAGE =_int32(6)
    IMAQ_QR_CELL_FILTER_MODE_ALL              =_int32(8)
    IMAQ_QR_CELL_FILTER_MODE_SIZE_GUARD       =_int32(0x7FFFFFFF)
dQRCellFilterMode={a.name:a.value for a in QRCellFilterMode}
drQRCellFilterMode={a.value:a.name for a in QRCellFilterMode}


class QRCellSampleSize(enum.IntEnum):
    IMAQ_QR_CELL_SAMPLE_SIZE_AUTO_DETECT=_int32((-2))
    IMAQ_QR_CELL_SAMPLE_SIZE1X1         =_int32(1)
    IMAQ_QR_CELL_SAMPLE_SIZE2X2         =_int32(2)
    IMAQ_QR_CELL_SAMPLE_SIZE3X3         =_int32(3)
    IMAQ_QR_CELL_SAMPLE_SIZE4X4         =_int32(4)
    IMAQ_QR_CELL_SAMPLE_SIZE5X5         =_int32(5)
    IMAQ_QR_CELL_SAMPLE_SIZE6X6         =_int32(6)
    IMAQ_QR_CELL_SAMPLE_SIZE7X7         =_int32(7)
    IMAQ_QR_CELL_SAMPLE_TYPE_SIZE_GUARD =_int32(0x7FFFFFFF)
dQRCellSampleSize={a.name:a.value for a in QRCellSampleSize}
drQRCellSampleSize={a.value:a.name for a in QRCellSampleSize}


class QRDemodulationMode(enum.IntEnum):
    IMAQ_QR_DEMODULATION_MODE_AUTO_DETECT   =_int32((-2))
    IMAQ_QR_DEMODULATION_MODE_HISTOGRAM     =_int32(0)
    IMAQ_QR_DEMODULATION_MODE_LOCAL_CONTRAST=_int32(1)
    IMAQ_QR_DEMODULATION_MODE_COMBINED      =_int32(2)
    IMAQ_QR_DEMODULATION_MODE_ALL           =_int32(3)
    IMAQ_QR_DEMODULATION_MODE_SIZE_GUARD    =_int32(0x7FFFFFFF)
dQRDemodulationMode={a.name:a.value for a in QRDemodulationMode}
drQRDemodulationMode={a.value:a.name for a in QRDemodulationMode}


class QRMirrorMode(enum.IntEnum):
    IMAQ_QR_MIRROR_MODE_AUTO_DETECT=_int32((-2))
    IMAQ_QR_MIRROR_MODE_MIRRORED   =_int32(1)
    IMAQ_QR_MIRROR_MODE_NORMAL     =_int32(0)
    IMAQ_QR_MIRROR_MODE_SIZE_GUARD =_int32(0x7FFFFFFF)
dQRMirrorMode={a.name:a.value for a in QRMirrorMode}
drQRMirrorMode={a.value:a.name for a in QRMirrorMode}


class QRPolarities(enum.IntEnum):
    IMAQ_QR_POLARITY_AUTO_DETECT    =_int32((-2))
    IMAQ_QR_POLARITY_BLACK_ON_WHITE =_int32(0)
    IMAQ_QR_POLARITY_WHITE_ON_BLACK =_int32(1)
    IMAQ_QR_POLARITY_MODE_SIZE_GUARD=_int32(0x7FFFFFFF)
dQRPolarities={a.name:a.value for a in QRPolarities}
drQRPolarities={a.value:a.name for a in QRPolarities}


class ReadClassifierFileMode(enum.IntEnum):
    IMAQ_CLASSIFIER_READ_ALL                  =_int32(0)
    IMAQ_CLASSIFIER_READ_SAMPLES              =_int32(1)
    IMAQ_CLASSIFIER_READ_PROPERTIES           =_int32(2)
    IMAQ_READ_CLASSIFIER_FILE_MODES_SIZE_GUARD=_int32(0xFFFFFFFF)
dReadClassifierFileMode={a.name:a.value for a in ReadClassifierFileMode}
drReadClassifierFileMode={a.value:a.name for a in ReadClassifierFileMode}


class FindReferenceDirection(enum.IntEnum):
    IMAQ_LEFT_TO_RIGHT_DIRECT         =_int32(0)
    IMAQ_LEFT_TO_RIGHT_INDIRECT       =_int32(1)
    IMAQ_TOP_TO_BOTTOM_DIRECT         =_int32(2)
    IMAQ_TOP_TO_BOTTOM_INDIRECT       =_int32(3)
    IMAQ_RIGHT_TO_LEFT_DIRECT         =_int32(4)
    IMAQ_RIGHT_TO_LEFT_INDIRECT       =_int32(5)
    IMAQ_BOTTOM_TO_TOP_DIRECT         =_int32(6)
    IMAQ_BOTTOM_TO_TOP_INDIRECT       =_int32(7)
    IMAQ_FIND_COORD_SYS_DIR_SIZE_GUARD=_int32(0xFFFFFFFF)
dFindReferenceDirection={a.name:a.value for a in FindReferenceDirection}
drFindReferenceDirection={a.value:a.name for a in FindReferenceDirection}


class CalibrationThumbnailType(enum.IntEnum):
    IMAQ_CAMARA_MODEL_TYPE                    =_int32(0)
    IMAQ_PERSPECTIVE_TYPE                     =_int32(1)
    IMAQ_MICRO_PLANE_TYPE                     =_int32(2)
    IMAQ_CALIBRATION_THUMBNAIL_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dCalibrationThumbnailType={a.name:a.value for a in CalibrationThumbnailType}
drCalibrationThumbnailType={a.value:a.name for a in CalibrationThumbnailType}


class StereoBlockMatchMetric(enum.IntEnum):
    IMAQ_SUM_ABSOLUTE_DIFF     =_int32(0)
    IMAQ_SUM_SQUARED_DIFF      =_int32(1)
    IMAQ_CORRELATION           =_int32(2)
    IMAQ_MATCH_METRIC_IS_AN_INT=_int32(0xFFFFFFFF)
dStereoBlockMatchMetric={a.name:a.value for a in StereoBlockMatchMetric}
drStereoBlockMatchMetric={a.value:a.name for a in StereoBlockMatchMetric}


class StereoPrefilterType(enum.IntEnum):
    IMAQ_STEREO_BM_NONE               =_int32(0)
    IMAQ_STEREO_BM_NORMALIZED_RESPONSE=_int32(1)
    IMAQ_STEREO_BM_XSOBEL             =_int32(2)
    IMAQ_PREFILTER_TYPE_IS_AN_INT     =_int32(0xFFFFFFFF)
dStereoPrefilterType={a.name:a.value for a in StereoPrefilterType}
drStereoPrefilterType={a.value:a.name for a in StereoPrefilterType}


class StereoCameraPosition(enum.IntEnum):
    IMAQ_STEREO_LEFT                     =_int32(0)
    IMAQ_STEREO_RIGHT                    =_int32(1)
    IMAQ_STEREO_CENTER                   =_int32(2)
    IMAQ_STEREO_CAMERA_POSITION_IS_AN_INT=_int32(0xFFFFFFFF)
dStereoCameraPosition={a.name:a.value for a in StereoCameraPosition}
drStereoCameraPosition={a.value:a.name for a in StereoCameraPosition}


class StereoSessionWriteOptions(enum.IntEnum):
    IMAQ_KWRITE_OPTIONS_FIRST       =_int32((-1))
    IMAQ_KFULL                      =_int32(0)
    IMAQ_COMPACT                    =_int32(1)
    IMAQ_WRITEOPTIONS_LAST          =_int32(2)
    IMAQ_SURE_WRITEOPTIONS_IS_AN_INT=_int32(0x7FFFFFFF)
dStereoSessionWriteOptions={a.name:a.value for a in StereoSessionWriteOptions}
drStereoSessionWriteOptions={a.value:a.name for a in StereoSessionWriteOptions}


class DataMatrixAdvancedProcessing(enum.IntEnum):
    IMAQ_START_OF_PROCESSING                   =_int32((-1))
    IMAQ_LINE_DETECTION                        =_int32(0)
    IMAQ_HIGHLIGHT_FILTER                      =_int32(1)
    IMAQ_AGGRESSIVE_PROCESSING                 =_int32(2)
    IMAQ_ENABLEFNC1                            =_int32(3)
    IMAQ_REFINE_BOUNDING_BOX                   =_int32(4)
    IMAQ_END_OF_PROCESSING                     =_int32(5)
    IMAQ_MAKE_SURE_ADVANCEDPROCESSING_IS_AN_INT=_int32(0x7FFFFFFF)
dDataMatrixAdvancedProcessing={a.name:a.value for a in DataMatrixAdvancedProcessing}
drDataMatrixAdvancedProcessing={a.value:a.name for a in DataMatrixAdvancedProcessing}


class RadialCoefficients(enum.IntEnum):
    IMAQ_COEFF_K1            =_int32(0)
    IMAQ_COEFF_K1_K2_K3      =_int32(1)
    IMAQ_COEFF_K1_K2_K3_K4_K5=_int32(2)
    IMAQ_COEFF_SIZE_GUARD    =_int32(0xFFFFFFFF)
dRadialCoefficients={a.name:a.value for a in RadialCoefficients}
drRadialCoefficients={a.value:a.name for a in RadialCoefficients}


class CalibrationMode2(enum.IntEnum):
    IMAQ_PERSPECTIVE_MODE            =_int32(0)
    IMAQ_MICROPLANE_MODE             =_int32(1)
    IMAQ_SIMPLE_CALIBRATION_MODE     =_int32(2)
    IMAQ_CORRECTED_IMAGE_MODE        =_int32(3)
    IMAQ_NO_CALIBRATION_MODE         =_int32(4)
    IMAQ_CALIBRATION_MODE2_SIZE_GUARD=_int32(0xFFFFFFFF)
dCalibrationMode2={a.name:a.value for a in CalibrationMode2}
drCalibrationMode2={a.value:a.name for a in CalibrationMode2}


class ParticleClassifierThresholdType(enum.IntEnum):
    IMAQ_THRESHOLD_MANUAL                           =_int32(0)
    IMAQ_THRESHOLD_AUTO                             =_int32(1)
    IMAQ_THRESHOLD_LOCAL                            =_int32(2)
    IMAQ_PARTICLECLASSIFIER_THRESHOLDTYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dParticleClassifierThresholdType={a.name:a.value for a in ParticleClassifierThresholdType}
drParticleClassifierThresholdType={a.value:a.name for a in ParticleClassifierThresholdType}


class DistortionModel(enum.IntEnum):
    IMAQ_NO_DISTORTION_MODEL        =_int32((-1))
    IMAQ_POLYNOMIAL_MODEL           =_int32(0)
    IMAQ_DIVISION_MODEL             =_int32(1)
    IMAQ_DISTORTION_MODEL_SIZE_GUARD=_int32(0X7FFFFFFF)
dDistortionModel={a.name:a.value for a in DistortionModel}
drDistortionModel={a.value:a.name for a in DistortionModel}


class StraightEdgeSearchMode(enum.IntEnum):
    IMAQ_USE_FIRST_RAKE_EDGES           =_int32(0)
    IMAQ_USE_BEST_RAKE_EDGES            =_int32(1)
    IMAQ_USE_BEST_HOUGH_LINE            =_int32(2)
    IMAQ_USE_FIRST_PROJECTION_EDGE      =_int32(3)
    IMAQ_USE_BEST_PROJECTION_EDGE       =_int32(4)
    IMAQ_STRAIGHT_EDGE_SEARCH_SIZE_GUARD=_int32(0xFFFFFFFF)
dStraightEdgeSearchMode={a.name:a.value for a in StraightEdgeSearchMode}
drStraightEdgeSearchMode={a.value:a.name for a in StraightEdgeSearchMode}


class SettingType(enum.IntEnum):
    IMAQ_ROTATION_ANGLE_RANGE   =_int32(0)
    IMAQ_SCALE_RANGE            =_int32(1)
    IMAQ_OCCLUSION_RANGE        =_int32(2)
    IMAQ_SETTING_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dSettingType={a.name:a.value for a in SettingType}
drSettingType={a.value:a.name for a in SettingType}


class SegmentationDistanceLevel(enum.IntEnum):
    IMAQ_SEGMENTATION_LEVEL_CONSERVATIVE=_int32(0)
    IMAQ_SEGMENTATION_LEVEL_AGGRESSIVE  =_int32(1)
    IMAQ_SEGMENTATION_LEVEL_SIZE_GUARD  =_int32(0xFFFFFFFF)
dSegmentationDistanceLevel={a.name:a.value for a in SegmentationDistanceLevel}
drSegmentationDistanceLevel={a.value:a.name for a in SegmentationDistanceLevel}


class ExtractContourSelection(enum.IntEnum):
    IMAQ_CLOSEST                             =_int32(0)
    IMAQ_LONGEST                             =_int32(1)
    IMAQ_STRONGEST                           =_int32(2)
    IMAQ_EXTRACT_CONTOUR_SELECTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dExtractContourSelection={a.name:a.value for a in ExtractContourSelection}
drExtractContourSelection={a.value:a.name for a in ExtractContourSelection}


class ConnectionConstraintType(enum.IntEnum):
    IMAQ_DISTANCE_CONSTRAINT             =_int32(0)
    IMAQ_ANGLE_CONSTRAINT                =_int32(1)
    IMAQ_CONNECTIVITY_CONSTRAINT         =_int32(2)
    IMAQ_GRADIENT_CONSTRAINT             =_int32(3)
    IMAQ_NUM_CONNECTION_CONSTRAINT_TYPES =_int32(4)
    IMAQ_CONNECTION_CONSTRAINT_SIZE_GUARD=_int32(0xFFFFFFFF)
dConnectionConstraintType={a.name:a.value for a in ConnectionConstraintType}
drConnectionConstraintType={a.value:a.name for a in ConnectionConstraintType}


class ExtractContourDirection(enum.IntEnum):
    IMAQ_RECT_LEFT_RIGHT                     =_int32(0)
    IMAQ_RECT_RIGHT_LEFT                     =_int32(1)
    IMAQ_RECT_TOP_BOTTOM                     =_int32(2)
    IMAQ_RECT_BOTTOM_TOP                     =_int32(3)
    IMAQ_ANNULUS_INNER_OUTER                 =_int32(4)
    IMAQ_ANNULUS_OUTER_INNER                 =_int32(5)
    IMAQ_ANNULUS_START_STOP                  =_int32(6)
    IMAQ_ANNULUS_STOP_START                  =_int32(7)
    IMAQ_EXTRACT_CONTOUR_DIRECTION_SIZE_GUARD=_int32(0xFFFFFFFF)
dExtractContourDirection={a.name:a.value for a in ExtractContourDirection}
drExtractContourDirection={a.value:a.name for a in ExtractContourDirection}


class RakeProcessType(enum.IntEnum):
    IMAQ_GET_FIRST_EDGES             =_int32(0)
    IMAQ_GET_FIRST_AND_LAST_EDGES    =_int32(1)
    IMAQ_GET_ALL_EDGES               =_int32(2)
    IMAQ_GET_BEST_EDGES              =_int32(3)
    IMAQ_RAKE_PROCESS_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dRakeProcessType={a.name:a.value for a in RakeProcessType}
drRakeProcessType={a.value:a.name for a in RakeProcessType}


class Connectivity(enum.IntEnum):
    IMAQ_FOUR_CONNECTED         =_int32(0)
    IMAQ_EIGHT_CONNECTED        =_int32(1)
    IMAQ_CONNECTIVITY_SIZE_GUARD=_int32(0xFFFFFFFF)
dConnectivity={a.name:a.value for a in Connectivity}
drConnectivity={a.value:a.name for a in Connectivity}


class GeometricSetupDataItem(enum.IntEnum):
    IMAQ_ENABLE_SUBPIXEL_ACCURACY          =_int32(10)
    IMAQ_SUBPIXEL_ITERATIONS               =_int32(11)
    IMAQ_SUBPIXEL_TOLERANCE                =_int32(12)
    IMAQ_INITIAL_MATCH_LIST_LENGTH         =_int32(13)
    IMAQ_MINIMUM_MATCH_SEPARATION_DISTANCE =_int32(15)
    IMAQ_MINIMUM_MATCH_SEPARATION_ANGLE    =_int32(16)
    IMAQ_MINIMUM_MATCH_SEPARATION_SCALE    =_int32(17)
    IMAQ_MAXIMUM_MATCH_OVERLAP             =_int32(18)
    IMAQ_ENABLE_COARSE_RESULT              =_int32(19)
    IMAQ_ENABLE_CALIBRATION_SUPPORT        =_int32(20)
    IMAQ_ENABLE_CONTRAST_REVERSAL          =_int32(21)
    IMAQ_SEARCH_STRATEGY                   =_int32(22)
    IMAQ_REFINEMENT_MATCH_FACTOR           =_int32(23)
    IMAQ_SUBPIXEL_MATCH_FACTOR             =_int32(24)
    IMAQ_MAX_REFINEMENT_ITERATIONS         =_int32(25)
    IMAQ_SCORING_METHOD                    =_int32(26)
    IMAQ_INITIAL_MATCH_ANGULAR_ACCURACY    =_int32(27)
    IMAQ_CURVE_EXTRACTION_MODE             =_int32(0)
    IMAQ_CURVE_EDGE_THRSHOLD               =_int32(1)
    IMAQ_CURVE_EDGE_FILTER                 =_int32(2)
    IMAQ_MINIMUM_CURVE_LENGTH              =_int32(3)
    IMAQ_CURVE_ROW_SEARCH_STEP_SIZE        =_int32(4)
    IMAQ_CURVE_COL_SEARCH_STEP_SIZE        =_int32(5)
    IMAQ_CURVE_MAX_END_POINT_GAP           =_int32(6)
    IMAQ_EXTRACT_CLOSED_CURVES             =_int32(7)
    IMAQ_ENABLE_SUBPIXEL_CURVE_EXTRACTION  =_int32(8)
    IMAQ_ENABLE_CORRELATION_SCORE          =_int32(9)
    IMAQ_ENABLE_TARGET_TEMPLATE_CURVESCORE =_int32(14)
    IMAQ_ENABLE_DEFECT_MAP                 =_int32(28)
    IMAQ_GEOMETRIC_SETUPDATA_ITEMSIZE_GUARD=_int32(0xFFFFFFFF)
dGeometricSetupDataItem={a.name:a.value for a in GeometricSetupDataItem}
drGeometricSetupDataItem={a.value:a.name for a in GeometricSetupDataItem}


class DataMatrixSubtype(enum.IntEnum):
    IMAQ_ALL_DATA_MATRIX_SUBTYPES            =_int32(0)
    IMAQ_DATA_MATRIX_SUBTYPES_ECC_000_ECC_140=_int32(1)
    IMAQ_DATA_MATRIX_SUBTYPE_ECC_200         =_int32(2)
    IMAQ_DATA_MATRIX_SUBTYPE_SIZE_GUARD      =_int32(0xFFFFFFFF)
dDataMatrixSubtype={a.name:a.value for a in DataMatrixSubtype}
drDataMatrixSubtype={a.value:a.name for a in DataMatrixSubtype}


class QRRotationMode(enum.IntEnum):
    IMAQ_QR_ROTATION_MODE_UNLIMITED  =_int32(0)
    IMAQ_QR_ROTATION_MODE_0_DEGREES  =_int32(1)
    IMAQ_QR_ROTATION_MODE_90_DEGREES =_int32(2)
    IMAQ_QR_ROTATION_MODE_180_DEGREES=_int32(3)
    IMAQ_QR_ROTATION_MODE_270_DEGREES=_int32(4)
    IMAQ_QR_ROTATION_MODE_SIZE_GUARD =_int32(0xFFFFFFFF)
dQRRotationMode={a.name:a.value for a in QRRotationMode}
drQRRotationMode={a.value:a.name for a in QRRotationMode}


class FlattenType(enum.IntEnum):
    IMAQ_FLATTEN_IMAGE                =_int32(0)
    IMAQ_FLATTEN_IMAGE_AND_VISION_INFO=_int32(1)
    IMAQ_FLATTEN_TYPE_SIZE_GUARD      =_int32(0xFFFFFFFF)
dFlattenType={a.name:a.value for a in FlattenType}
drFlattenType={a.value:a.name for a in FlattenType}


class LocalThresholdMethod(enum.IntEnum):
    IMAQ_NIBLACK                          =_int32(0)
    IMAQ_BACKGROUND_CORRECTION            =_int32(1)
    IMAQ_SAUVOLA                          =_int32(2)
    IMAQ_MODIFIED_SAUVOLA                 =_int32(3)
    IMAQ_LOCAL_THRESHOLD_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dLocalThresholdMethod={a.name:a.value for a in LocalThresholdMethod}
drLocalThresholdMethod={a.value:a.name for a in LocalThresholdMethod}


class FeatureType(enum.IntEnum):
    IMAQ_NOT_FOUND_FEATURE                  =_int32(0)
    IMAQ_CIRCLE_FEATURE                     =_int32(1)
    IMAQ_ELLIPSE_FEATURE                    =_int32(2)
    IMAQ_CONST_CURVE_FEATURE                =_int32(3)
    IMAQ_RECTANGLE_FEATURE                  =_int32(4)
    IMAQ_LEG_FEATURE                        =_int32(5)
    IMAQ_CORNER_FEATURE                     =_int32(6)
    IMAQ_PARALLEL_LINE_PAIR_FEATURE         =_int32(7)
    IMAQ_PAIR_OF_PARALLEL_LINE_PAIRS_FEATURE=_int32(8)
    IMAQ_LINE_FEATURE                       =_int32(9)
    IMAQ_CLOSED_CURVE_FEATURE               =_int32(10)
    IMAQ_FEATURE_TYPE_SIZE_GUARD            =_int32(0xFFFFFFFF)
dFeatureType={a.name:a.value for a in FeatureType}
drFeatureType={a.value:a.name for a in FeatureType}


class WindowBackgroundHatchStyle(enum.IntEnum):
    IMAQ_HATCH_STYLE_HORIZONTAL       =_int32(0)
    IMAQ_HATCH_STYLE_VERTICAL         =_int32(1)
    IMAQ_HATCH_STYLE_FORWARD_DIAGONAL =_int32(2)
    IMAQ_HATCH_STYLE_BACKWARD_DIAGONAL=_int32(3)
    IMAQ_HATCH_STYLE_CROSS            =_int32(4)
    IMAQ_HATCH_STYLE_CROSS_HATCH      =_int32(5)
    IMAQ_HATCH_STYLE_SIZE_GUARD       =_int32(0xFFFFFFFF)
dWindowBackgroundHatchStyle={a.name:a.value for a in WindowBackgroundHatchStyle}
drWindowBackgroundHatchStyle={a.value:a.name for a in WindowBackgroundHatchStyle}


class WindowBackgroundFillStyle(enum.IntEnum):
    IMAQ_FILL_STYLE_SOLID     =_int32(0)
    IMAQ_FILL_STYLE_HATCH     =_int32(2)
    IMAQ_FILL_STYLE_DEFAULT   =_int32(3)
    IMAQ_FILL_STYLE_SIZE_GUARD=_int32(0xFFFFFFFF)
dWindowBackgroundFillStyle={a.name:a.value for a in WindowBackgroundFillStyle}
drWindowBackgroundFillStyle={a.value:a.name for a in WindowBackgroundFillStyle}


class ExtractionMode(enum.IntEnum):
    IMAQ_NORMAL_IMAGE              =_int32(0)
    IMAQ_UNIFORM_REGIONS           =_int32(1)
    IMAQ_EXTRACTION_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dExtractionMode={a.name:a.value for a in ExtractionMode}
drExtractionMode={a.value:a.name for a in ExtractionMode}


class LinearAveragesMode(enum.IntEnum):
    IMAQ_COLUMN_AVERAGES                =_int32(1)
    IMAQ_ROW_AVERAGES                   =_int32(2)
    IMAQ_RISING_DIAGONAL_AVERAGES       =_int32(4)
    IMAQ_FALLING_DIAGONAL_AVERAGES      =_int32(8)
    IMAQ_ALL_LINEAR_AVERAGES            =_int32(15)
    IMAQ_LINEAR_AVERAGES_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dLinearAveragesMode={a.name:a.value for a in LinearAveragesMode}
drLinearAveragesMode={a.value:a.name for a in LinearAveragesMode}


class Barcode2DSearchMode(enum.IntEnum):
    IMAQ_SEARCH_MULTIPLE                  =_int32(0)
    IMAQ_SEARCH_SINGLE_CONSERVATIVE       =_int32(1)
    IMAQ_SEARCH_SINGLE_AGGRESSIVE         =_int32(2)
    IMAQ_BARCODE_2D_SEARCH_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dBarcode2DSearchMode={a.name:a.value for a in Barcode2DSearchMode}
drBarcode2DSearchMode={a.value:a.name for a in Barcode2DSearchMode}


class RegistrationMethod(enum.IntEnum):
    IMAQ_REGISTRATION_NONE       =_int32(0)
    IMAQ_REGISTRATION_PERSPECTIVE=_int32(1)
    IMAQ_REGISTRATION_SIZE_GUARD =_int32(0xFFFFFFFF)
dRegistrationMethod={a.name:a.value for a in RegistrationMethod}
drRegistrationMethod={a.value:a.name for a in RegistrationMethod}


class Barcode2DShape(enum.IntEnum):
    IMAQ_SQUARE_BARCODE_2D          =_int32(0)
    IMAQ_RECTANGULAR_BARCODE_2D     =_int32(1)
    IMAQ_BARCODE_2D_SHAPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dBarcode2DShape={a.name:a.value for a in Barcode2DShape}
drBarcode2DShape={a.value:a.name for a in Barcode2DShape}


class Barcode2DCellShape(enum.IntEnum):
    IMAQ_SQUARE_CELLS                    =_int32(0)
    IMAQ_ROUND_CELLS                     =_int32(1)
    IMAQ_BARCODE_2D_CELL_SHAPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dBarcode2DCellShape={a.name:a.value for a in Barcode2DCellShape}
drBarcode2DCellShape={a.value:a.name for a in Barcode2DCellShape}


class Barcode2DContrast(enum.IntEnum):
    IMAQ_ALL_BARCODE_2D_CONTRASTS      =_int32(0)
    IMAQ_BLACK_ON_WHITE_BARCODE_2D     =_int32(1)
    IMAQ_WHITE_ON_BLACK_BARCODE_2D     =_int32(2)
    IMAQ_BARCODE_2D_CONTRAST_SIZE_GUARD=_int32(0xFFFFFFFF)
dBarcode2DContrast={a.name:a.value for a in Barcode2DContrast}
drBarcode2DContrast={a.value:a.name for a in Barcode2DContrast}


class Barcode2DType(enum.IntEnum):
    IMAQ_PDF417                    =_int32(0)
    IMAQ_DATA_MATRIX_ECC_000       =_int32(1)
    IMAQ_DATA_MATRIX_ECC_050       =_int32(2)
    IMAQ_DATA_MATRIX_ECC_080       =_int32(3)
    IMAQ_DATA_MATRIX_ECC_100       =_int32(4)
    IMAQ_DATA_MATRIX_ECC_140       =_int32(5)
    IMAQ_DATA_MATRIX_ECC_200       =_int32(6)
    IMAQ_BARCODE_2D_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dBarcode2DType={a.name:a.value for a in Barcode2DType}
drBarcode2DType={a.value:a.name for a in Barcode2DType}


class ClassifierEngineType(enum.IntEnum):
    IMAQ_ENGINE_NONE                      =_int32(0)
    IMAQ_ENGINE_NEAREST_NEIGHBOR          =_int32(1)
    IMAQ_ENGINE_SUPPORT_VECTOR_MACHINE    =_int32(2)
    IMAQ_CLASSIFIER_ENGINE_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dClassifierEngineType={a.name:a.value for a in ClassifierEngineType}
drClassifierEngineType={a.value:a.name for a in ClassifierEngineType}


class ClassifierType(enum.IntEnum):
    IMAQ_CLASSIFIER_CUSTOM         =_int32(0)
    IMAQ_CLASSIFIER_PARTICLE       =_int32(1)
    IMAQ_CLASSIFIER_COLOR          =_int32(2)
    IMAQ_CLASSIFIER_TEXTURE        =_int32(3)
    IMAQ_CLASSIFIER_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dClassifierType={a.name:a.value for a in ClassifierType}
drClassifierType={a.value:a.name for a in ClassifierType}


class StereoInterpolationType(enum.IntEnum):
    IMAQ_KIPTYPEZEROORDER       =_int32(0)
    IMAQ_KIPTYPEBILINEAR        =_int32(1)
    IMAQ_KIPTYPEQUADRATIC       =_int32(2)
    IMAQ_kIPTYPECUBICSPLINE     =_int32(3)
    IMAQ_KIPTYPEBILINEARFIXED   =_int32(4)
    IMAQ_INTERPLOATION_IS_AN_INT=_int32(888)
dStereoInterpolationType={a.name:a.value for a in StereoInterpolationType}
drStereoInterpolationType={a.value:a.name for a in StereoInterpolationType}


class EdgeFilterSize(enum.IntEnum):
    IMAQ_FINE                       =_int32(0)
    IMAQ_NORMAL                     =_int32(1)
    IMAQ_CONTOUR_TRACING            =_int32(2)
    IMAQ_EDGE_FILTER_SIZE_SIZE_GUARD=_int32(0xFFFFFFFF)
dEdgeFilterSize={a.name:a.value for a in EdgeFilterSize}
drEdgeFilterSize={a.value:a.name for a in EdgeFilterSize}


class DataMatrixPolarity(enum.IntEnum):
    IMAQ_AUTO_DETECT_POLARITY           =_int32((-2))
    IMAQ_BLACK_DATA_ON_WHITE_BACKGROUND =_int32(0)
    IMAQ_WHITE_DATA_ON_BLACK_BACKGROUND =_int32(1)
    IMAQ_DATA_MATRIX_POLARITY_SIZE_GUARD=_int32(0x7FFFFFFF)
dDataMatrixPolarity={a.name:a.value for a in DataMatrixPolarity}
drDataMatrixPolarity={a.value:a.name for a in DataMatrixPolarity}


class SearchDirection(enum.IntEnum):
    IMAQ_SEARCH_DIRECTION_LEFT_TO_RIGHT=_int32(0)
    IMAQ_SEARCH_DIRECTION_RIGHT_TO_LEFT=_int32(1)
    IMAQ_SEARCH_DIRECTION_TOP_TO_BOTTOM=_int32(2)
    IMAQ_SEARCH_DIRECTION_BOTTOM_TO_TOP=_int32(3)
    IMAQ_SEARCH_DIRECTION_SIZE_GUARD   =_int32(0xFFFFFFFF)
dSearchDirection={a.name:a.value for a in SearchDirection}
drSearchDirection={a.value:a.name for a in SearchDirection}


class QRStreamMode(enum.IntEnum):
    IMAQ_QR_MODE_NUMERIC     =_int32(0)
    IMAQ_QR_MODE_ALPHANUMERIC=_int32(1)
    IMAQ_QR_MODE_RAW_BYTE    =_int32(2)
    IMAQ_QR_MODE_EAN128_TOKEN=_int32(3)
    IMAQ_QR_MODE_EAN128_DATA =_int32(4)
    IMAQ_QR_MODE_ECI         =_int32(5)
    IMAQ_QR_MODE_KANJI       =_int32(6)
    IMAQ_QR_MODE_SIZE_GUARD  =_int32(0xFFFFFFFF)
dQRStreamMode={a.name:a.value for a in QRStreamMode}
drQRStreamMode={a.value:a.name for a in QRStreamMode}


class QRModelType(enum.IntEnum):
    IMAQ_QR_MODELTYPE_AUTO_DETECT=_int32(0)
    IMAQ_QR_MODELTYPE_MICRO      =_int32(1)
    IMAQ_QR_MODELTYPE_MODEL1     =_int32(2)
    IMAQ_QR_MODELTYPE_MODEL2     =_int32(3)
    IMAQ_QR_MODEL_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dQRModelType={a.name:a.value for a in QRModelType}
drQRModelType={a.value:a.name for a in QRModelType}


class ColumnProcessingMode(enum.IntEnum):
    IMAQ_AVERAGE_COLUMNS                  =_int32(0)
    IMAQ_MEDIAN_COLUMNS                   =_int32(1)
    IMAQ_COLUMN_PROCESSING_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dColumnProcessingMode={a.name:a.value for a in ColumnProcessingMode}
drColumnProcessingMode={a.value:a.name for a in ColumnProcessingMode}


class EdgePolaritySearchMode(enum.IntEnum):
    IMAQ_SEARCH_FOR_ALL_EDGES         =_int32(0)
    IMAQ_SEARCH_FOR_RISING_EDGES      =_int32(1)
    IMAQ_SEARCH_FOR_FALLING_EDGES     =_int32(2)
    IMAQ_EDGE_POLARITY_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dEdgePolaritySearchMode={a.name:a.value for a in EdgePolaritySearchMode}
drEdgePolaritySearchMode={a.value:a.name for a in EdgePolaritySearchMode}


class AIMGrade(enum.IntEnum):
    IMAQ_AIM_GRADE_F                     =_int32(0)
    IMAQ_AIM_GRADE_D                     =_int32(1)
    IMAQ_AIM_GRADE_C                     =_int32(2)
    IMAQ_AIM_GRADE_B                     =_int32(3)
    IMAQ_AIM_GRADE_A                     =_int32(4)
    IMAQ_DATA_MATRIX_AIM_GRADE_SIZE_GUARD=_int32(0xFFFFFFFF)
dAIMGrade={a.name:a.value for a in AIMGrade}
drAIMGrade={a.value:a.name for a in AIMGrade}


class DataMatrixCellFillMode(enum.IntEnum):
    IMAQ_AUTO_DETECT_CELL_FILL_MODE           =_int32((-2))
    IMAQ_LOW_FILL                             =_int32(0)
    IMAQ_NORMAL_FILL                          =_int32(1)
    IMAQ_DATA_MATRIX_CELL_FILL_MODE_SIZE_GUARD=_int32(0x7FFFFFFF)
dDataMatrixCellFillMode={a.name:a.value for a in DataMatrixCellFillMode}
drDataMatrixCellFillMode={a.value:a.name for a in DataMatrixCellFillMode}


class CompressionType(enum.IntEnum):
    IMAQ_COMPRESSION_NONE           =_int32(0)
    IMAQ_COMPRESSION_JPEG           =_int32(1)
    IMAQ_COMPRESSION_PACKED_BINARY  =_int32(2)
    IMAQ_COMPRESSION_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dCompressionType={a.name:a.value for a in CompressionType}
drCompressionType={a.value:a.name for a in CompressionType}


class DataMatrixECC(enum.IntEnum):
    IMAQ_AUTO_DETECT_ECC           =_int32((-2))
    IMAQ_ECC_000                   =_int32(0)
    IMAQ_ECC_050                   =_int32(50)
    IMAQ_ECC_080                   =_int32(80)
    IMAQ_ECC_100                   =_int32(100)
    IMAQ_ECC_140                   =_int32(140)
    IMAQ_ECC_000_140               =_int32(190)
    IMAQ_ECC_200                   =_int32(200)
    IMAQ_DATA_MATRIX_ECC_SIZE_GUARD=_int32(0x7FFFFFFF)
dDataMatrixECC={a.name:a.value for a in DataMatrixECC}
drDataMatrixECC={a.value:a.name for a in DataMatrixECC}


class VisionInfoType2(enum.IntEnum):
    IMAQ_VISIONINFO_CALIBRATION             =_int32(0x01)
    IMAQ_VISIONINFO_OVERLAY                 =_int32(0x02)
    IMAQ_VISIONINFO_GRAYTEMPLATE            =_int32(0x04)
    IMAQ_VISIONINFO_COLORTEMPLATE           =_int32(0x08)
    IMAQ_VISIONINFO_GEOMETRICTEMPLATE       =_int32(0x10)
    IMAQ_VISIONINFO_CUSTOMDATA              =_int32(0x20)
    IMAQ_VISIONINFO_GOLDENTEMPLATE          =_int32(0x40)
    IMAQ_VISIONINFO_GEOMETRICTEMPLATE2      =_int32(0x80)
    IMAQ_VISIONINFO_CONTOURDATA             =_int32(0x100)
    IMAQ_VISIONINFO_CAMERAMODEL             =_int32(0x200)
    IMAQ_VISIONINFO_PYRAMIDGRAYVALUETEMPLATE=_int32(0x400)
    IMAQ_VISIONINFO_PYRAMIDGRADIENTTEMPLATE =_int32(0x800)
    IMAQ_VISIONINFO_ALL                     =_int32(0xFFFFFFFF)
dVisionInfoType2={a.name:a.value for a in VisionInfoType2}
drVisionInfoType2={a.value:a.name for a in VisionInfoType2}


class DataMatrixCellFilterMode(enum.IntEnum):
    IMAQ_AUTO_DETECT_CELL_FILTER_MODE           =_int32((-2))
    IMAQ_AVERAGE_FILTER                         =_int32(0)
    IMAQ_MEDIAN_FILTER                          =_int32(1)
    IMAQ_CENTRAL_AVERAGE_FILTER                 =_int32(2)
    IMAQ_HIGH_AVERAGE_FILTER                    =_int32(3)
    IMAQ_LOW_AVERAGE_FILTER                     =_int32(4)
    IMAQ_VERY_HIGH_AVERAGE_FILTER               =_int32(5)
    IMAQ_VERY_LOW_AVERAGE_FILTER                =_int32(6)
    IMAQ_ALL_CELL_FILTERS                       =_int32(8)
    IMAQ_DATA_MATRIX_CELL_FILTER_MODE_SIZE_GUARD=_int32(0x7FFFFFFF)
dDataMatrixCellFilterMode={a.name:a.value for a in DataMatrixCellFilterMode}
drDataMatrixCellFilterMode={a.value:a.name for a in DataMatrixCellFilterMode}


class DataMatrixCellSampleSize(enum.IntEnum):
    IMAQ_AUTO_DETECT_CELL_SAMPLE_SIZE           =_int32((-2))
    IMAQ_1x1                                    =_int32(1)
    IMAQ_2x2                                    =_int32(2)
    IMAQ_3x3                                    =_int32(3)
    IMAQ_4x4                                    =_int32(4)
    IMAQ_5x5                                    =_int32(5)
    IMAQ_6x6                                    =_int32(6)
    IMAQ_7x7                                    =_int32(7)
    IMAQ_DATA_MATRIX_CELL_SAMPLE_SIZE_SIZE_GUARD=_int32(0x7FFFFFFF)
dDataMatrixCellSampleSize={a.name:a.value for a in DataMatrixCellSampleSize}
drDataMatrixCellSampleSize={a.value:a.name for a in DataMatrixCellSampleSize}


class DataMatrixMirrorMode(enum.IntEnum):
    IMAQ_AUTO_DETECT_MIRROR                =_int32((-2))
    IMAQ_APPEARS_NORMAL                    =_int32(0)
    IMAQ_APPEARS_MIRRORED                  =_int32(1)
    IMAQ_DATA_MATRIX_MIRROR_MODE_SIZE_GUARD=_int32(0x7FFFFFFF)
dDataMatrixMirrorMode={a.name:a.value for a in DataMatrixMirrorMode}
drDataMatrixMirrorMode={a.value:a.name for a in DataMatrixMirrorMode}


class DataMatrixRotationMode(enum.IntEnum):
    IMAQ_UNLIMITED_ROTATION                  =_int32(0)
    IMAQ_0_DEGREES                           =_int32(1)
    IMAQ_90_DEGREES                          =_int32(2)
    IMAQ_180_DEGREES                         =_int32(3)
    IMAQ_270_DEGREES                         =_int32(4)
    IMAQ_DATA_MATRIX_ROTATION_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dDataMatrixRotationMode={a.name:a.value for a in DataMatrixRotationMode}
drDataMatrixRotationMode={a.value:a.name for a in DataMatrixRotationMode}


class DataMatrixGradingMode(enum.IntEnum):
    IMAQ_NO_GRADING                         =_int32(0)
    IMAQ_PREPARE_FOR_AIM                    =_int32(1)
    IMAQ_DATA_MATRIX_GRADING_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dDataMatrixGradingMode={a.name:a.value for a in DataMatrixGradingMode}
drDataMatrixGradingMode={a.value:a.name for a in DataMatrixGradingMode}


class WaveletTransformMode(enum.IntEnum):
    IMAQ_WAVELET_TRANSFORM_INTEGER        =_int32(0)
    IMAQ_WAVELET_TRANSFORM_FLOATING_POINT =_int32(1)
    IMAQ_WAVELET_TRANSFORM_MODE_SIZE_GUARD=_int32(0xFFFFFFFF)
dWaveletTransformMode={a.name:a.value for a in WaveletTransformMode}
drWaveletTransformMode={a.value:a.name for a in WaveletTransformMode}


class NormalizationMethod(enum.IntEnum):
    IMAQ_NORMALIZATION_NONE              =_int32(0)
    IMAQ_NORMALIZATION_HISTOGRAM_MATCHING=_int32(1)
    IMAQ_NORMALIZATION_AVERAGE_MATCHING  =_int32(2)
    IMAQ_NORMALIZATION_SIZE_GUARD        =_int32(0xFFFFFFFF)
dNormalizationMethod={a.name:a.value for a in NormalizationMethod}
drNormalizationMethod={a.value:a.name for a in NormalizationMethod}


class DataMatrixDemodulationMode(enum.IntEnum):
    IMAQ_AUTO_DETECT_DEMODULATION_MODE           =_int32((-2))
    IMAQ_HISTOGRAM                               =_int32(0)
    IMAQ_LOCAL_CONTRAST                          =_int32(1)
    IMAQ_COMBINED                                =_int32(2)
    IMAQ_ALL_DEMODULATION_MODES                  =_int32(3)
    IMAQ_DATA_MATRIX_DEMODULATION_MODE_SIZE_GUARD=_int32(0x7FFFFFFF)
dDataMatrixDemodulationMode={a.name:a.value for a in DataMatrixDemodulationMode}
drDataMatrixDemodulationMode={a.value:a.name for a in DataMatrixDemodulationMode}


class RTVideoModeOperation(enum.IntEnum):
    IMAQ_GET_MODE                =_int32(0)
    IMAQ_SET_MODE                =_int32(1)
    IMAQ_RT_VIDEO_MODE_SIZE_GUARD=_int32(0XFFFFFFFF)
dRTVideoModeOperation={a.name:a.value for a in RTVideoModeOperation}
drRTVideoModeOperation={a.value:a.name for a in RTVideoModeOperation}


class RTDisplayVideoMode(enum.IntEnum):
    IMAQ_TEXT_MODE                    =_int32(0)
    IMAQ_GRAPHICS_MODE                =_int32(1)
    IMAQ_DISPLAY_VIDEO_MODE_SIZE_GUARD=_int32(0XFFFFFFFF)
dRTDisplayVideoMode={a.name:a.value for a in RTDisplayVideoMode}
drRTDisplayVideoMode={a.value:a.name for a in RTDisplayVideoMode}


class BGEstimateMethod(enum.IntEnum):
    IMAQ_MODEL                       =_int32(0)
    IMAQ_BG_CORRECTION               =_int32(1)
    IMAQ_BG_NIBLACK                  =_int32(2)
    IMAQ_BGESTIMATE_METHOD_SIZE_GUARD=_int32(0xFFFFFFFF)
dBGEstimateMethod={a.name:a.value for a in BGEstimateMethod}
drBGEstimateMethod={a.value:a.name for a in BGEstimateMethod}


class SVMType(enum.IntEnum):
    IMAQ_C_SVC             =_int32(0)
    IMAQ_NU_SVC            =_int32(1)
    IMAQ_ONE_CLASS         =_int32(2)
    IMAQ_IMAQ_SVMTYPE_GUARD=_int32(0xFFFFFFFF)
dSVMType={a.name:a.value for a in SVMType}
drSVMType={a.value:a.name for a in SVMType}


class KernelType(enum.IntEnum):
    IMAQ_LINEARSVM       =_int32(0)
    IMAQ_POLYNOMIAL      =_int32(1)
    IMAQ_GAUSSIAN        =_int32(2)
    IMAQ_RBF             =_int32(3)
    IMAQ_KERNELTYPE_GUARD=_int32(0xFFFFFFFF)
dKernelType={a.name:a.value for a in KernelType}
drKernelType={a.value:a.name for a in KernelType}


class CornerOperators(enum.IntEnum):
    IMAQ_HARRISCORNER         =_int32(0)
    IMAQ_SHICORNER            =_int32(1)
    IMAQ_CORNEROPERATORS_GUARD=_int32(0xFFFFFFFF)
dCornerOperators={a.name:a.value for a in CornerOperators}
drCornerOperators={a.value:a.name for a in CornerOperators}


class VelocityRepresentation(enum.IntEnum):
    IMAQ_CARTESIAN                         =_int32(0)
    IMAQ_POLAR                             =_int32(1)
    IMAQ_VELOCITY_REPRESENTATION_SIZE_GUARD=_int32(0XFFFFFFFF)
dVelocityRepresentation={a.name:a.value for a in VelocityRepresentation}
drVelocityRepresentation={a.value:a.name for a in VelocityRepresentation}


class StoppingType(enum.IntEnum):
    IMAQ_ITERATIONS             =_int32(1)
    IMAQ_EPSILON                =_int32(2)
    IMAQ_BOTH                   =_int32(3)
    IMAQ_STOPPINGTYPE_SIZE_GUARD=_int32(0XFFFFFFFF)
dStoppingType={a.name:a.value for a in StoppingType}
drStoppingType={a.value:a.name for a in StoppingType}


class ObjectTrackingMethod(enum.IntEnum):
    IMAQ_MEANSHIFTTRADITIONAL           =_int32(0)
    IMAQ_SHAPEADAPTEDMEANSHIFT          =_int32(1)
    IMAQ_OBJECTTRACKINGMETHOD_SIZE_GUARD=_int32(0XFFFFFFFF)
dObjectTrackingMethod={a.name:a.value for a in ObjectTrackingMethod}
drObjectTrackingMethod={a.value:a.name for a in ObjectTrackingMethod}


class ObjectDescriptionMethod(enum.IntEnum):
    IMAQ_HISTOGRAMBASED                    =_int32(0)
    IMAQ_OBJECTDESCRIPTIONMETHOD_SIZE_GUARD=_int32(0XFFFFFFFF)
dObjectDescriptionMethod={a.name:a.value for a in ObjectDescriptionMethod}
drObjectDescriptionMethod={a.value:a.name for a in ObjectDescriptionMethod}


class InterchangeObjectTrackingMethods(enum.IntEnum):
    IMAQ_NOCHANGE                                   =_int32(0)
    IMAQ_MSTOMS                                     =_int32(1)
    IMAQ_MSTOEMS                                    =_int32(2)
    IMAQ_EMSTOMS                                    =_int32(3)
    IMAQ_EMSTOEMS                                   =_int32(4)
    IMAQ_INTERCHANGEOBJECTTRACKINGMETHODS_SIZE_GUARD=_int32(0XFFFFFFFF)
dInterchangeObjectTrackingMethods={a.name:a.value for a in InterchangeObjectTrackingMethods}
drInterchangeObjectTrackingMethods={a.value:a.name for a in InterchangeObjectTrackingMethods}


class FeatureExtractionMethods(enum.IntEnum):
    IMAQ_HOG                                =_int32(0)
    IMAQ_LBP                                =_int32(1)
    IMAQ_FEATUREEXTRACTIONMETHODS_SIZE_GUARD=_int32(0XFFFFFFFF)
dFeatureExtractionMethods={a.name:a.value for a in FeatureExtractionMethods}
drFeatureExtractionMethods={a.value:a.name for a in FeatureExtractionMethods}


class FeatureDescriptionMethods(enum.IntEnum):
    IMAQ_FREAK                              =_int32(0)
    IMAQ_BRISK                              =_int32(1)
    IMAQ_FEATUREDESCRIPTIONMETHODS_SIZEGUARD=_int32(0XFFFFFFFF)
dFeatureDescriptionMethods={a.name:a.value for a in FeatureDescriptionMethods}
drFeatureDescriptionMethods={a.value:a.name for a in FeatureDescriptionMethods}


ContourID=ctypes.c_int
uInt32=ctypes.c_uint
SESSION_ID=uInt32
AVISession=ctypes.c_int
FilterName=ctypes.c_char_p
String255=ctypes.c_char*256
AVI2Session=ctypes.c_void_p
int64=__int64
class StereoLearnCalibQualiy(ctypes.Structure):
    _fields_=[  ("dProjectionError",ctypes.c_double),
                ("dcalibQuality",ctypes.c_double),
                ("dmaxRectError",ctypes.c_double),
                ("drectQuality",ctypes.c_double) ]
PStereoLearnCalibQualiy=ctypes.POINTER(StereoLearnCalibQualiy)
class CStereoLearnCalibQualiy(ctypes_wrap.CStructWrapper):
    _struct=StereoLearnCalibQualiy


class StereoRtfSettings(ctypes.Structure):
    _fields_=[  ("iLearnLookup",ctypes.c_uint),
                ("iRenderToOriginalImage",ctypes.c_uint),
                ("iScalingFactor",ctypes.c_uint) ]
PStereoRtfSettings=ctypes.POINTER(StereoRtfSettings)
class CStereoRtfSettings(ctypes_wrap.CStructWrapper):
    _struct=StereoRtfSettings


class StereoPrefilterOptions(ctypes.Structure):
    _fields_=[  ("filterType",ctypes.c_int),
                ("filterSize",ctypes.c_uint),
                ("filterCap",ctypes.c_uint) ]
PStereoPrefilterOptions=ctypes.POINTER(StereoPrefilterOptions)
class CStereoPrefilterOptions(ctypes_wrap.CStructWrapper):
    _struct=StereoPrefilterOptions


class StereoBlockMatchingOptions(ctypes.Structure):
    _fields_=[  ("metric",ctypes.c_int),
                ("windowSize",ctypes.c_uint),
                ("minDisparity",ctypes.c_int),
                ("numDisparities",ctypes.c_uint),
                ("maxLeftRightDisparityDiff",ctypes.c_int),
                ("subpixel",ctypes.c_short),
                ("pixelReplaceVal",ctypes.c_float) ]
PStereoBlockMatchingOptions=ctypes.POINTER(StereoBlockMatchingOptions)
class CStereoBlockMatchingOptions(ctypes_wrap.CStructWrapper):
    _struct=StereoBlockMatchingOptions


class StereoSGBlockMatchingOptions(ctypes.Structure):
    _fields_=[  ("metric",ctypes.c_int),
                ("windowSize",ctypes.c_uint),
                ("minDisparity",ctypes.c_uint),
                ("numDisparities",ctypes.c_uint),
                ("p1",ctypes.c_int),
                ("p2",ctypes.c_int),
                ("fullDP",ctypes.c_short),
                ("maxLeftRightDisparityDiff",ctypes.c_int),
                ("subpixel",ctypes.c_short),
                ("pixelReplaceVal",ctypes.c_float) ]
PStereoSGBlockMatchingOptions=ctypes.POINTER(StereoSGBlockMatchingOptions)
class CStereoSGBlockMatchingOptions(ctypes_wrap.CStructWrapper):
    _struct=StereoSGBlockMatchingOptions


class StereoDepthControl(ctypes.Structure):
    _fields_=[  ("dMinDepth",ctypes.c_double),
                ("dMaxDepth",ctypes.c_double) ]
PStereoDepthControl=ctypes.POINTER(StereoDepthControl)
class CStereoDepthControl(ctypes_wrap.CStructWrapper):
    _struct=StereoDepthControl


class StereoPostfilterOptions(ctypes.Structure):
    _fields_=[  ("textureThreshold",ctypes.c_uint),
                ("uniquenessRatio",ctypes.c_uint),
                ("speckleWindowSize",ctypes.c_uint),
                ("speckleRange",ctypes.c_uint) ]
PStereoPostfilterOptions=ctypes.POINTER(StereoPostfilterOptions)
class CStereoPostfilterOptions(ctypes_wrap.CStructWrapper):
    _struct=StereoPostfilterOptions


class StereoCoordPtFloat(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_float),
                ("y",ctypes.c_float) ]
PStereoCoordPtFloat=ctypes.POINTER(StereoCoordPtFloat)
class CStereoCoordPtFloat(ctypes_wrap.CStructWrapper):
    _struct=StereoCoordPtFloat


class StereoPointDbl3D(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_double),
                ("y",ctypes.c_double),
                ("z",ctypes.c_double) ]
PStereoPointDbl3D=ctypes.POINTER(StereoPointDbl3D)
class CStereoPointDbl3D(ctypes_wrap.CStructWrapper):
    _struct=StereoPointDbl3D


class Range(ctypes.Structure):
    _fields_=[  ("minValue",ctypes.c_int),
                ("maxValue",ctypes.c_int) ]
PRange=ctypes.POINTER(Range)
class CRange(ctypes_wrap.CStructWrapper):
    _struct=Range


class OCRSpacingOptions2(ctypes.Structure):
    _fields_=[  ("minCharSpacing",ctypes.c_int),
                ("minCharSize",ctypes.c_int),
                ("maxCharSize",ctypes.c_int),
                ("maxHorizontalElementSpacing",ctypes.c_int),
                ("maxVerticalElementSpacing",ctypes.c_int),
                ("minBoundingRectWidth",ctypes.c_int),
                ("maxBoundingRectWidth",ctypes.c_int),
                ("minBoundingRectHeight",ctypes.c_int),
                ("maxBoundingRectHeight",ctypes.c_int),
                ("autoSplit",ctypes.c_int),
                ("textLocation",ctypes.c_int),
                ("lineSeparator",ctypes.c_int),
                ("shortestPathSegment",ctypes.c_int),
                ("minPixelsForSpace",ctypes.c_int) ]
POCRSpacingOptions2=ctypes.POINTER(OCRSpacingOptions2)
class COCRSpacingOptions2(ctypes_wrap.CStructWrapper):
    _struct=OCRSpacingOptions2


class OCRProcessingOptions2(ctypes.Structure):
    _fields_=[  ("thresholdType",ctypes.c_int),
                ("mode",ctypes.c_int),
                ("lowThreshold",ctypes.c_int),
                ("highThreshold",ctypes.c_int),
                ("blockCount",ctypes.c_int),
                ("fastThreshold",ctypes.c_int),
                ("biModalCalculation",ctypes.c_int),
                ("darkCharacters",ctypes.c_int),
                ("windowWidth",ctypes.c_uint),
                ("windowHeight",ctypes.c_uint),
                ("colorMode",ctypes.c_int),
                ("plane1Range",Range),
                ("plane2Range",Range),
                ("plane3Range",Range),
                ("removeParticlesTouchingROI",ctypes.c_int),
                ("erosionCount",ctypes.c_int) ]
POCRProcessingOptions2=ctypes.POINTER(OCRProcessingOptions2)
class COCRProcessingOptions2(ctypes_wrap.CStructWrapper):
    _struct=OCRProcessingOptions2


class CharacterStatistics(ctypes.Structure):
    _fields_=[  ("left",ctypes.c_int),
                ("top",ctypes.c_int),
                ("width",ctypes.c_int),
                ("height",ctypes.c_int),
                ("characterSize",ctypes.c_int) ]
PCharacterStatistics=ctypes.POINTER(CharacterStatistics)
class CCharacterStatistics(ctypes_wrap.CStructWrapper):
    _struct=CharacterStatistics


class CharReport3(ctypes.Structure):
    _fields_=[  ("character",ctypes.c_char_p),
                ("classificationScore",ctypes.c_int),
                ("verificationScore",ctypes.c_int),
                ("verified",ctypes.c_int),
                ("lowThreshold",ctypes.c_int),
                ("highThreshold",ctypes.c_int),
                ("characterStats",CharacterStatistics) ]
PCharReport3=ctypes.POINTER(CharReport3)
class CCharReport3(ctypes_wrap.CStructWrapper):
    _struct=CharReport3


class ReadTextReport4(ctypes.Structure):
    _fields_=[  ("readString",ctypes.c_char_p),
                ("characterReport",ctypes.POINTER(CharReport3)),
                ("numCharacterReports",ctypes.c_int),
                ("roiBoundingCharacters",ctypes.c_void_p),
                ("numberOflinesDetected",ctypes.c_int) ]
PReadTextReport4=ctypes.POINTER(ReadTextReport4)
class CReadTextReport4(ctypes_wrap.CStructWrapper):
    _struct=ReadTextReport4


class CalibReflectanceStruct(ctypes.Structure):
    _fields_=[  ("rcal",ctypes.c_double),
                ("srcal",ctypes.c_double),
                ("mlcal",ctypes.c_double),
                ("srtarget",ctypes.c_double) ]
PCalibReflectanceStruct=ctypes.POINTER(CalibReflectanceStruct)
class CCalibReflectanceStruct(ctypes_wrap.CStructWrapper):
    _struct=CalibReflectanceStruct


class AdvancedDataMatrixOptions(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("value",ctypes.c_double) ]
PAdvancedDataMatrixOptions=ctypes.POINTER(AdvancedDataMatrixOptions)
class CAdvancedDataMatrixOptions(ctypes_wrap.CStructWrapper):
    _struct=AdvancedDataMatrixOptions


class AIMDPMGradeReport(ctypes.Structure):
    _fields_=[  ("overallGrade",ctypes.c_int),
                ("decodingGrade",ctypes.c_int),
                ("cellContrastGrade",ctypes.c_int),
                ("cellContrast",ctypes.c_float),
                ("printGrowthGrade",ctypes.c_int),
                ("printGrowth",ctypes.c_float),
                ("axialNonuniformityGrade",ctypes.c_int),
                ("axialNonuniformity",ctypes.c_float),
                ("unusedErrorCorrectionGrade",ctypes.c_int),
                ("unusedErrorCorrection",ctypes.c_float),
                ("gridNonUniformityGrade",ctypes.c_int),
                ("gridNonUniformity",ctypes.c_float),
                ("cellModulationGrade",ctypes.c_int),
                ("fixedPatternDamageGrade",ctypes.c_int),
                ("fixedPatternDamage",ctypes.c_float),
                ("minimumReflectanceGrade",ctypes.c_int),
                ("minimumReflectance",ctypes.c_float) ]
PAIMDPMGradeReport=ctypes.POINTER(AIMDPMGradeReport)
class CAIMDPMGradeReport(ctypes_wrap.CStructWrapper):
    _struct=AIMDPMGradeReport


class GradeReportISO15415(ctypes.Structure):
    _fields_=[  ("overallGrade",ctypes.c_int),
                ("decodingGrade",ctypes.c_int),
                ("symbolContrastGrade",ctypes.c_int),
                ("symbolContrast",ctypes.c_float),
                ("printGrowthGrade",ctypes.c_int),
                ("printGrowth",ctypes.c_float),
                ("axialNonuniformityGrade",ctypes.c_int),
                ("axialNonuniformity",ctypes.c_float),
                ("unusedErrorCorrectionGrade",ctypes.c_int),
                ("unusedErrorCorrection",ctypes.c_float),
                ("gridNonUniformityGrade",ctypes.c_int),
                ("gridNonUniformity",ctypes.c_float),
                ("modulationGrade",ctypes.c_int),
                ("fixedPatternDamageGrade",ctypes.c_int),
                ("fixedPatternDamage",ctypes.c_float) ]
PGradeReportISO15415=ctypes.POINTER(GradeReportISO15415)
class CGradeReportISO15415(ctypes_wrap.CStructWrapper):
    _struct=GradeReportISO15415


class GradeReportISO16022(ctypes.Structure):
    _fields_=[  ("overallGrade",ctypes.c_int),
                ("decodingGrade",ctypes.c_int),
                ("symbolContrastGrade",ctypes.c_int),
                ("symbolContrast",ctypes.c_float),
                ("printGrowthGrade",ctypes.c_int),
                ("printGrowth",ctypes.c_float),
                ("axialNonuniformityGrade",ctypes.c_int),
                ("axialNonuniformity",ctypes.c_float),
                ("unusedErrorCorrectionGrade",ctypes.c_int),
                ("unusedErrorCorrection",ctypes.c_float) ]
PGradeReportISO16022=ctypes.POINTER(GradeReportISO16022)
class CGradeReportISO16022(ctypes_wrap.CStructWrapper):
    _struct=GradeReportISO16022


class CalibrationCorrectionLearnSetupInfo(ctypes.Structure):
    _fields_=[  ("scaleMode",ctypes.c_int),
                ("roiMode",ctypes.c_int),
                ("learnCorrectionTable",ctypes.c_char) ]
PCalibrationCorrectionLearnSetupInfo=ctypes.POINTER(CalibrationCorrectionLearnSetupInfo)
class CCalibrationCorrectionLearnSetupInfo(ctypes_wrap.CStructWrapper):
    _struct=CalibrationCorrectionLearnSetupInfo


class CalibrationModelSetup(ctypes.Structure):
    _fields_=[  ("distortionModel",ctypes.c_int),
                ("radialCoefficient",ctypes.c_int),
                ("tangentialCoefficients",ctypes.c_int) ]
PCalibrationModelSetup=ctypes.POINTER(CalibrationModelSetup)
class CCalibrationModelSetup(ctypes_wrap.CStructWrapper):
    _struct=CalibrationModelSetup


class DivisionModel(ctypes.Structure):
    _fields_=[  ("kappa",ctypes.c_float) ]
PDivisionModel=ctypes.POINTER(DivisionModel)
class CDivisionModel(ctypes_wrap.CStructWrapper):
    _struct=DivisionModel


class FocalLength(ctypes.Structure):
    _fields_=[  ("fx",ctypes.c_float),
                ("fy",ctypes.c_float) ]
PFocalLength=ctypes.POINTER(FocalLength)
class CFocalLength(ctypes_wrap.CStructWrapper):
    _struct=FocalLength


class PolyModel(ctypes.Structure):
    _fields_=[  ("kCoeffs",ctypes.POINTER(ctypes.c_float)),
                ("numKCoeffs",ctypes.c_uint),
                ("p1",ctypes.c_float),
                ("p2",ctypes.c_float) ]
PPolyModel=ctypes.POINTER(PolyModel)
class CPolyModel(ctypes_wrap.CStructWrapper):
    _struct=PolyModel


class DistortionModelParams(ctypes.Structure):
    _fields_=[  ("distortionModel",ctypes.c_int),
                ("polyModel",PolyModel),
                ("divisionModel",DivisionModel) ]
PDistortionModelParams=ctypes.POINTER(DistortionModelParams)
class CDistortionModelParams(ctypes_wrap.CStructWrapper):
    _struct=DistortionModelParams


class PointFloat(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_float),
                ("y",ctypes.c_float) ]
PPointFloat=ctypes.POINTER(PointFloat)
class CPointFloat(ctypes_wrap.CStructWrapper):
    _struct=PointFloat


class InternalParameters(ctypes.Structure):
    _fields_=[  ("isInsufficientData",ctypes.c_char),
                ("focalLength",FocalLength),
                ("opticalCenter",PointFloat) ]
PInternalParameters=ctypes.POINTER(InternalParameters)
class CInternalParameters(ctypes_wrap.CStructWrapper):
    _struct=InternalParameters


class MaxGridSize(ctypes.Structure):
    _fields_=[  ("xMax",ctypes.c_uint),
                ("yMax",ctypes.c_uint) ]
PMaxGridSize=ctypes.POINTER(MaxGridSize)
class CMaxGridSize(ctypes_wrap.CStructWrapper):
    _struct=MaxGridSize


class ImageSize(ctypes.Structure):
    _fields_=[  ("xRes",ctypes.c_uint),
                ("yRes",ctypes.c_uint) ]
PImageSize=ctypes.POINTER(ImageSize)
class CImageSize(ctypes_wrap.CStructWrapper):
    _struct=ImageSize


class PointDouble(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_double),
                ("y",ctypes.c_double) ]
PPointDouble=ctypes.POINTER(PointDouble)
class CPointDouble(ctypes_wrap.CStructWrapper):
    _struct=PointDouble


class CalibrationReferencePoints(ctypes.Structure):
    _fields_=[  ("pixelCoords",ctypes.POINTER(PointDouble)),
                ("numPixelCoords",ctypes.c_uint),
                ("realCoords",ctypes.POINTER(PointDouble)),
                ("numRealCoords",ctypes.c_uint),
                ("units",ctypes.c_int),
                ("imageSize",ImageSize) ]
PCalibrationReferencePoints=ctypes.POINTER(CalibrationReferencePoints)
class CCalibrationReferencePoints(ctypes_wrap.CStructWrapper):
    _struct=CalibrationReferencePoints


class GetCameraParametersReport(ctypes.Structure):
    _fields_=[  ("projectionMatrix",ctypes.POINTER(ctypes.c_double)),
                ("projectionMatrixRows",ctypes.c_size_t),
                ("projectionMatrixCols",ctypes.c_size_t),
                ("distortion",DistortionModelParams),
                ("internalParams",InternalParameters) ]
PGetCameraParametersReport=ctypes.POINTER(GetCameraParametersReport)
class CGetCameraParametersReport(ctypes_wrap.CStructWrapper):
    _struct=GetCameraParametersReport


class CalibrationAxisInfo(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("rotationAngle",ctypes.c_float),
                ("axisDirection",ctypes.c_int) ]
PCalibrationAxisInfo=ctypes.POINTER(CalibrationAxisInfo)
class CCalibrationAxisInfo(ctypes_wrap.CStructWrapper):
    _struct=CalibrationAxisInfo


class CalibrationLearnSetupInfo(ctypes.Structure):
    _fields_=[  ("calibrationMethod",ctypes.c_int),
                ("distortionModel",ctypes.c_int),
                ("scaleMode",ctypes.c_int),
                ("roiMode",ctypes.c_int),
                ("learnCorrectionTable",ctypes.c_char) ]
PCalibrationLearnSetupInfo=ctypes.POINTER(CalibrationLearnSetupInfo)
class CCalibrationLearnSetupInfo(ctypes_wrap.CStructWrapper):
    _struct=CalibrationLearnSetupInfo


class GridDescriptor(ctypes.Structure):
    _fields_=[  ("xStep",ctypes.c_float),
                ("yStep",ctypes.c_float),
                ("unit",ctypes.c_int) ]
PGridDescriptor=ctypes.POINTER(GridDescriptor)
class CGridDescriptor(ctypes_wrap.CStructWrapper):
    _struct=GridDescriptor


class ErrorStatistics(ctypes.Structure):
    _fields_=[  ("mean",ctypes.c_double),
                ("maximum",ctypes.c_double),
                ("standardDeviation",ctypes.c_double),
                ("distortion",ctypes.c_double) ]
PErrorStatistics=ctypes.POINTER(ErrorStatistics)
class CErrorStatistics(ctypes_wrap.CStructWrapper):
    _struct=ErrorStatistics


class GetCalibrationInfoReport(ctypes.Structure):
    _fields_=[  ("userRoi",ctypes.c_void_p),
                ("calibrationRoi",ctypes.c_void_p),
                ("axisInfo",CalibrationAxisInfo),
                ("learnSetupInfo",CalibrationLearnSetupInfo),
                ("gridDescriptor",GridDescriptor),
                ("errorMap",ctypes.POINTER(ctypes.c_float)),
                ("errorMapRows",ctypes.c_size_t),
                ("errorMapCols",ctypes.c_size_t),
                ("errorStatistics",ErrorStatistics) ]
PGetCalibrationInfoReport=ctypes.POINTER(GetCalibrationInfoReport)
class CGetCalibrationInfoReport(ctypes_wrap.CStructWrapper):
    _struct=GetCalibrationInfoReport


class EdgePolarity(ctypes.Structure):
    _fields_=[  ("start",ctypes.c_int),
                ("end",ctypes.c_int) ]
PEdgePolarity=ctypes.POINTER(EdgePolarity)
class CEdgePolarity(ctypes_wrap.CStructWrapper):
    _struct=EdgePolarity


class ClampSettings(ctypes.Structure):
    _fields_=[  ("angleRange",ctypes.c_double),
                ("edgePolarity",EdgePolarity) ]
PClampSettings=ctypes.POINTER(ClampSettings)
class CClampSettings(ctypes_wrap.CStructWrapper):
    _struct=ClampSettings


class PointDoublePair(ctypes.Structure):
    _fields_=[  ("start",PointDouble),
                ("end",PointDouble) ]
PPointDoublePair=ctypes.POINTER(PointDoublePair)
class CPointDoublePair(ctypes_wrap.CStructWrapper):
    _struct=PointDoublePair


class ClampResults(ctypes.Structure):
    _fields_=[  ("distancePix",ctypes.c_double),
                ("distanceRealWorld",ctypes.c_double),
                ("angleAbs",ctypes.c_double),
                ("angleRelative",ctypes.c_double) ]
PClampResults=ctypes.POINTER(ClampResults)
class CClampResults(ctypes_wrap.CStructWrapper):
    _struct=ClampResults


class ClampPoints(ctypes.Structure):
    _fields_=[  ("pixel",PointDoublePair),
                ("realWorld",PointDoublePair) ]
PClampPoints=ctypes.POINTER(ClampPoints)
class CClampPoints(ctypes_wrap.CStructWrapper):
    _struct=ClampPoints


class RGBValue(ctypes.Structure):
    _fields_=[  ("B",ctypes.c_ubyte),
                ("G",ctypes.c_ubyte),
                ("R",ctypes.c_ubyte),
                ("alpha",ctypes.c_ubyte) ]
PRGBValue=ctypes.POINTER(RGBValue)
class CRGBValue(ctypes_wrap.CStructWrapper):
    _struct=RGBValue


class ClampOverlaySettings(ctypes.Structure):
    _fields_=[  ("showSearchArea",ctypes.c_int),
                ("showCurves",ctypes.c_int),
                ("showClampLocation",ctypes.c_int),
                ("showResult",ctypes.c_int),
                ("searchAreaColor",RGBValue),
                ("curvesColor",RGBValue),
                ("clampLocationsColor",RGBValue),
                ("resultColor",RGBValue),
                ("overlayGroupName",ctypes.c_char_p) ]
PClampOverlaySettings=ctypes.POINTER(ClampOverlaySettings)
class CClampOverlaySettings(ctypes_wrap.CStructWrapper):
    _struct=ClampOverlaySettings


class ClampMax2Report(ctypes.Structure):
    _fields_=[  ("clampResults",ClampResults),
                ("clampPoints",ClampPoints),
                ("calibrationValid",ctypes.c_uint) ]
PClampMax2Report=ctypes.POINTER(ClampMax2Report)
class CClampMax2Report(ctypes_wrap.CStructWrapper):
    _struct=ClampMax2Report


class ContourFitSplineReport(ctypes.Structure):
    _fields_=[  ("points",ctypes.POINTER(PointDouble)),
                ("numberOfPoints",ctypes.c_int) ]
PContourFitSplineReport=ctypes.POINTER(ContourFitSplineReport)
class CContourFitSplineReport(ctypes_wrap.CStructWrapper):
    _struct=ContourFitSplineReport


class LineFloat(ctypes.Structure):
    _fields_=[  ("start",PointFloat),
                ("end",PointFloat) ]
PLineFloat=ctypes.POINTER(LineFloat)
class CLineFloat(ctypes_wrap.CStructWrapper):
    _struct=LineFloat


class BarcodeInfo2(ctypes.Structure):
    _fields_=[  ("data",ctypes.POINTER(ctypes.c_ubyte)),
                ("numdata",ctypes.c_uint),
                ("char1",ctypes.c_ubyte),
                ("char2",ctypes.c_ubyte),
                ("checkSums",ctypes.c_ubyte),
                ("type",ctypes.c_int),
                ("confidenceLevel",ctypes.c_float),
                ("boundingBox",ctypes.POINTER(PointFloat)),
                ("numBox",ctypes.c_uint) ]
PBarcodeInfo2=ctypes.POINTER(BarcodeInfo2)
class CBarcodeInfo2(ctypes_wrap.CStructWrapper):
    _struct=BarcodeInfo2


class Barcode1DSearchOptions(ctypes.Structure):
    _fields_=[  ("minBarcodeWidth",ctypes.c_uint),
                ("minEdgeStrength",ctypes.c_uint),
                ("minBars",ctypes.c_uint),
                ("skipLocationSearch",ctypes.c_int) ]
PBarcode1DSearchOptions=ctypes.POINTER(Barcode1DSearchOptions)
class CBarcode1DSearchOptions(ctypes_wrap.CStructWrapper):
    _struct=Barcode1DSearchOptions


class LineEquation(ctypes.Structure):
    _fields_=[  ("a",ctypes.c_double),
                ("b",ctypes.c_double),
                ("c",ctypes.c_double) ]
PLineEquation=ctypes.POINTER(LineEquation)
class CLineEquation(ctypes_wrap.CStructWrapper):
    _struct=LineEquation


class ContourFitLineReport(ctypes.Structure):
    _fields_=[  ("lineSegment",LineFloat),
                ("lineEquation",LineEquation) ]
PContourFitLineReport=ctypes.POINTER(ContourFitLineReport)
class CContourFitLineReport(ctypes_wrap.CStructWrapper):
    _struct=ContourFitLineReport


class ContourFitPolynomialReport(ctypes.Structure):
    _fields_=[  ("bestFit",ctypes.POINTER(PointDouble)),
                ("numberOfPoints",ctypes.c_int),
                ("polynomialCoefficients",ctypes.POINTER(ctypes.c_double)),
                ("numberOfCoefficients",ctypes.c_int) ]
PContourFitPolynomialReport=ctypes.POINTER(ContourFitPolynomialReport)
class CContourFitPolynomialReport(ctypes_wrap.CStructWrapper):
    _struct=ContourFitPolynomialReport


class CornerOption(ctypes.Structure):
    _fields_=[  ("detectorType",ctypes.c_int),
                ("kernelSize",ctypes.c_int),
                ("minCornerPointStrength",ctypes.c_double) ]
PCornerOption=ctypes.POINTER(CornerOption)
class CCornerOption(ctypes_wrap.CStructWrapper):
    _struct=CornerOption


class PartialCircle(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("radius",ctypes.c_double),
                ("startAngle",ctypes.c_double),
                ("endAngle",ctypes.c_double) ]
PPartialCircle=ctypes.POINTER(PartialCircle)
class CPartialCircle(ctypes_wrap.CStructWrapper):
    _struct=PartialCircle


class PartialEllipse(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("angle",ctypes.c_double),
                ("majorRadius",ctypes.c_double),
                ("minorRadius",ctypes.c_double),
                ("startAngle",ctypes.c_double),
                ("endAngle",ctypes.c_double) ]
PPartialEllipse=ctypes.POINTER(PartialEllipse)
class CPartialEllipse(ctypes_wrap.CStructWrapper):
    _struct=PartialEllipse


class SetupMatchPatternData(ctypes.Structure):
    _fields_=[  ("matchSetupData",ctypes.POINTER(ctypes.c_ubyte)),
                ("numMatchSetupData",ctypes.c_int) ]
PSetupMatchPatternData=ctypes.POINTER(SetupMatchPatternData)
class CSetupMatchPatternData(ctypes_wrap.CStructWrapper):
    _struct=SetupMatchPatternData


class RangeSettingDouble(ctypes.Structure):
    _fields_=[  ("settingType",ctypes.c_int),
                ("min",ctypes.c_double),
                ("max",ctypes.c_double) ]
PRangeSettingDouble=ctypes.POINTER(RangeSettingDouble)
class CRangeSettingDouble(ctypes_wrap.CStructWrapper):
    _struct=RangeSettingDouble


class GeometricAdvancedSetupDataOption(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("value",ctypes.c_double) ]
PGeometricAdvancedSetupDataOption=ctypes.POINTER(GeometricAdvancedSetupDataOption)
class CGeometricAdvancedSetupDataOption(ctypes_wrap.CStructWrapper):
    _struct=GeometricAdvancedSetupDataOption


class ContourInfoReport(ctypes.Structure):
    _fields_=[  ("pointsPixel",ctypes.POINTER(PointDouble)),
                ("numPointsPixel",ctypes.c_uint),
                ("pointsReal",ctypes.POINTER(PointDouble)),
                ("numPointsReal",ctypes.c_uint),
                ("curvaturePixel",ctypes.POINTER(ctypes.c_double)),
                ("numCurvaturePixel",ctypes.c_uint),
                ("curvatureReal",ctypes.POINTER(ctypes.c_double)),
                ("numCurvatureReal",ctypes.c_uint),
                ("length",ctypes.c_double),
                ("lengthReal",ctypes.c_double),
                ("hasEquation",ctypes.c_uint) ]
PContourInfoReport=ctypes.POINTER(ContourInfoReport)
class CContourInfoReport(ctypes_wrap.CStructWrapper):
    _struct=ContourInfoReport


class ROILabel(ctypes.Structure):
    _fields_=[  ("className",ctypes.c_char_p),
                ("label",ctypes.c_uint) ]
PROILabel=ctypes.POINTER(ROILabel)
class CROILabel(ctypes_wrap.CStructWrapper):
    _struct=ROILabel


class SupervisedColorSegmentationReport(ctypes.Structure):
    _fields_=[  ("labelOut",ctypes.POINTER(ROILabel)),
                ("numLabelOut",ctypes.c_uint) ]
PSupervisedColorSegmentationReport=ctypes.POINTER(SupervisedColorSegmentationReport)
class CSupervisedColorSegmentationReport(ctypes_wrap.CStructWrapper):
    _struct=SupervisedColorSegmentationReport


class LabelToROIReport(ctypes.Structure):
    _fields_=[  ("roiArray",ctypes.POINTER(ctypes.c_void_p)),
                ("numOfROIs",ctypes.c_uint),
                ("labelsOutArray",ctypes.POINTER(ctypes.c_uint)),
                ("numOfLabels",ctypes.c_uint),
                ("isTooManyVectorsArray",ctypes.POINTER(ctypes.c_int)),
                ("isTooManyVectorsArraySize",ctypes.c_uint) ]
PLabelToROIReport=ctypes.POINTER(LabelToROIReport)
class CLabelToROIReport(ctypes_wrap.CStructWrapper):
    _struct=LabelToROIReport


class ColorSegmenationOptions(ctypes.Structure):
    _fields_=[  ("windowX",ctypes.c_uint),
                ("windowY",ctypes.c_uint),
                ("stepSize",ctypes.c_uint),
                ("minParticleArea",ctypes.c_uint),
                ("maxParticleArea",ctypes.c_uint),
                ("isFineSegment",ctypes.c_short) ]
PColorSegmenationOptions=ctypes.POINTER(ColorSegmenationOptions)
class CColorSegmenationOptions(ctypes_wrap.CStructWrapper):
    _struct=ColorSegmenationOptions


class ClassifiedCurve(ctypes.Structure):
    _fields_=[  ("length",ctypes.c_double),
                ("lengthReal",ctypes.c_double),
                ("maxCurvature",ctypes.c_double),
                ("maxCurvatureReal",ctypes.c_double),
                ("label",ctypes.c_uint),
                ("curvePoints",ctypes.POINTER(PointDouble)),
                ("numCurvePoints",ctypes.c_uint) ]
PClassifiedCurve=ctypes.POINTER(ClassifiedCurve)
class CClassifiedCurve(ctypes_wrap.CStructWrapper):
    _struct=ClassifiedCurve


class RangeDouble(ctypes.Structure):
    _fields_=[  ("minValue",ctypes.c_double),
                ("maxValue",ctypes.c_double) ]
PRangeDouble=ctypes.POINTER(RangeDouble)
class CRangeDouble(ctypes_wrap.CStructWrapper):
    _struct=RangeDouble


class RangeLabel(ctypes.Structure):
    _fields_=[  ("range",RangeDouble),
                ("label",ctypes.c_uint) ]
PRangeLabel=ctypes.POINTER(RangeLabel)
class CRangeLabel(ctypes_wrap.CStructWrapper):
    _struct=RangeLabel


class CurvatureAnalysisReport(ctypes.Structure):
    _fields_=[  ("curves",ctypes.POINTER(ClassifiedCurve)),
                ("numCurves",ctypes.c_uint) ]
PCurvatureAnalysisReport=ctypes.POINTER(CurvatureAnalysisReport)
class CCurvatureAnalysisReport(ctypes_wrap.CStructWrapper):
    _struct=CurvatureAnalysisReport


class Disparity(ctypes.Structure):
    _fields_=[  ("current",PointDouble),
                ("reference",PointDouble),
                ("distance",ctypes.c_double) ]
PDisparity=ctypes.POINTER(Disparity)
class CDisparity(ctypes_wrap.CStructWrapper):
    _struct=Disparity


class ComputeDistancesReport(ctypes.Structure):
    _fields_=[  ("distances",ctypes.POINTER(Disparity)),
                ("numDistances",ctypes.c_uint),
                ("distancesReal",ctypes.POINTER(Disparity)),
                ("numDistancesReal",ctypes.c_uint) ]
PComputeDistancesReport=ctypes.POINTER(ComputeDistancesReport)
class CComputeDistancesReport(ctypes_wrap.CStructWrapper):
    _struct=ComputeDistancesReport


class MatchMode(ctypes.Structure):
    _fields_=[  ("rotation",ctypes.c_uint),
                ("scale",ctypes.c_uint),
                ("occlusion",ctypes.c_uint) ]
PMatchMode=ctypes.POINTER(MatchMode)
class CMatchMode(ctypes_wrap.CStructWrapper):
    _struct=MatchMode


class ClassifiedDisparity(ctypes.Structure):
    _fields_=[  ("length",ctypes.c_double),
                ("lengthReal",ctypes.c_double),
                ("maxDistance",ctypes.c_double),
                ("maxDistanceReal",ctypes.c_double),
                ("label",ctypes.c_uint),
                ("templateSubsection",ctypes.POINTER(PointDouble)),
                ("numTemplateSubsection",ctypes.c_uint),
                ("targetSubsection",ctypes.POINTER(PointDouble)),
                ("numTargetSubsection",ctypes.c_uint) ]
PClassifiedDisparity=ctypes.POINTER(ClassifiedDisparity)
class CClassifiedDisparity(ctypes_wrap.CStructWrapper):
    _struct=ClassifiedDisparity


class ClassifyDistancesReport(ctypes.Structure):
    _fields_=[  ("classifiedDistances",ctypes.POINTER(ClassifiedDisparity)),
                ("numClassifiedDistances",ctypes.c_uint) ]
PClassifyDistancesReport=ctypes.POINTER(ClassifyDistancesReport)
class CClassifyDistancesReport(ctypes_wrap.CStructWrapper):
    _struct=ClassifyDistancesReport


class ContourComputeCurvatureReport(ctypes.Structure):
    _fields_=[  ("curvaturePixel",ctypes.POINTER(ctypes.c_double)),
                ("numCurvaturePixel",ctypes.c_uint),
                ("curvatureReal",ctypes.POINTER(ctypes.c_double)),
                ("numCurvatureReal",ctypes.c_uint) ]
PContourComputeCurvatureReport=ctypes.POINTER(ContourComputeCurvatureReport)
class CContourComputeCurvatureReport(ctypes_wrap.CStructWrapper):
    _struct=ContourComputeCurvatureReport


class ContourOverlaySettings(ctypes.Structure):
    _fields_=[  ("overlay",ctypes.c_uint),
                ("color",RGBValue),
                ("width",ctypes.c_uint),
                ("maintainWidth",ctypes.c_uint) ]
PContourOverlaySettings=ctypes.POINTER(ContourOverlaySettings)
class CContourOverlaySettings(ctypes_wrap.CStructWrapper):
    _struct=ContourOverlaySettings


class CurveParameters(ctypes.Structure):
    _fields_=[  ("extractionMode",ctypes.c_int),
                ("threshold",ctypes.c_int),
                ("filterSize",ctypes.c_int),
                ("minLength",ctypes.c_int),
                ("searchStep",ctypes.c_int),
                ("maxEndPointGap",ctypes.c_int),
                ("subpixel",ctypes.c_int) ]
PCurveParameters=ctypes.POINTER(CurveParameters)
class CCurveParameters(ctypes_wrap.CStructWrapper):
    _struct=CurveParameters


class ExtractContourReport(ctypes.Structure):
    _fields_=[  ("contourPoints",ctypes.POINTER(PointDouble)),
                ("numContourPoints",ctypes.c_int),
                ("sourcePoints",ctypes.POINTER(PointDouble)),
                ("numSourcePoints",ctypes.c_int) ]
PExtractContourReport=ctypes.POINTER(ExtractContourReport)
class CExtractContourReport(ctypes_wrap.CStructWrapper):
    _struct=ExtractContourReport


class ConnectionConstraint(ctypes.Structure):
    _fields_=[  ("constraintType",ctypes.c_int),
                ("range",RangeDouble) ]
PConnectionConstraint=ctypes.POINTER(ConnectionConstraint)
class CConnectionConstraint(ctypes_wrap.CStructWrapper):
    _struct=ConnectionConstraint


class ExtractTextureFeaturesReport(ctypes.Structure):
    _fields_=[  ("waveletBands",ctypes.POINTER(ctypes.c_int)),
                ("numWaveletBands",ctypes.c_int),
                ("textureFeatures",ctypes.POINTER(ctypes.POINTER(ctypes.c_double))),
                ("textureFeaturesRows",ctypes.c_int),
                ("textureFeaturesCols",ctypes.c_int) ]
PExtractTextureFeaturesReport=ctypes.POINTER(ExtractTextureFeaturesReport)
class CExtractTextureFeaturesReport(ctypes_wrap.CStructWrapper):
    _struct=ExtractTextureFeaturesReport


class WaveletBandsReport(ctypes.Structure):
    _fields_=[  ("LLBand",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("LHBand",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("HLBand",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("HHBand",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("LLLBand",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("LLHBand",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("LHLBand",ctypes.c_float),
                ("LHHBand",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("rows",ctypes.c_int),
                ("cols",ctypes.c_int) ]
PWaveletBandsReport=ctypes.POINTER(WaveletBandsReport)
class CWaveletBandsReport(ctypes_wrap.CStructWrapper):
    _struct=WaveletBandsReport


class CircleFitOptions(ctypes.Structure):
    _fields_=[  ("maxRadius",ctypes.c_int),
                ("stepSize",ctypes.c_double),
                ("processType",ctypes.c_int) ]
PCircleFitOptions=ctypes.POINTER(CircleFitOptions)
class CCircleFitOptions(ctypes_wrap.CStructWrapper):
    _struct=CircleFitOptions


class EdgeOptions2(ctypes.Structure):
    _fields_=[  ("polarity",ctypes.c_int),
                ("kernelSize",ctypes.c_uint),
                ("width",ctypes.c_uint),
                ("minThreshold",ctypes.c_float),
                ("interpolationType",ctypes.c_int),
                ("columnProcessingMode",ctypes.c_int) ]
PEdgeOptions2=ctypes.POINTER(EdgeOptions2)
class CEdgeOptions2(ctypes_wrap.CStructWrapper):
    _struct=EdgeOptions2


class FindCircularEdgeOptions(ctypes.Structure):
    _fields_=[  ("direction",ctypes.c_int),
                ("showSearchArea",ctypes.c_int),
                ("showSearchLines",ctypes.c_int),
                ("showEdgesFound",ctypes.c_int),
                ("showResult",ctypes.c_int),
                ("searchAreaColor",RGBValue),
                ("searchLinesColor",RGBValue),
                ("searchEdgesColor",RGBValue),
                ("resultColor",RGBValue),
                ("overlayGroupName",ctypes.c_char_p),
                ("edgeOptions",EdgeOptions2) ]
PFindCircularEdgeOptions=ctypes.POINTER(FindCircularEdgeOptions)
class CFindCircularEdgeOptions(ctypes_wrap.CStructWrapper):
    _struct=FindCircularEdgeOptions


class FindConcentricEdgeOptions(ctypes.Structure):
    _fields_=[  ("direction",ctypes.c_int),
                ("showSearchArea",ctypes.c_int),
                ("showSearchLines",ctypes.c_int),
                ("showEdgesFound",ctypes.c_int),
                ("showResult",ctypes.c_int),
                ("searchAreaColor",RGBValue),
                ("searchLinesColor",RGBValue),
                ("searchEdgesColor",RGBValue),
                ("resultColor",RGBValue),
                ("overlayGroupName",ctypes.c_char_p),
                ("edgeOptions",EdgeOptions2) ]
PFindConcentricEdgeOptions=ctypes.POINTER(FindConcentricEdgeOptions)
class CFindConcentricEdgeOptions(ctypes_wrap.CStructWrapper):
    _struct=FindConcentricEdgeOptions


class ConcentricEdgeFitOptions(ctypes.Structure):
    _fields_=[  ("maxRadius",ctypes.c_int),
                ("stepSize",ctypes.c_double),
                ("processType",ctypes.c_int) ]
PConcentricEdgeFitOptions=ctypes.POINTER(ConcentricEdgeFitOptions)
class CConcentricEdgeFitOptions(ctypes_wrap.CStructWrapper):
    _struct=ConcentricEdgeFitOptions


class FindConcentricEdgeReport(ctypes.Structure):
    _fields_=[  ("startPt",PointFloat),
                ("endPt",PointFloat),
                ("startPtCalibrated",PointFloat),
                ("endPtCalibrated",PointFloat),
                ("angle",ctypes.c_double),
                ("angleCalibrated",ctypes.c_double),
                ("straightness",ctypes.c_double),
                ("avgStrength",ctypes.c_double),
                ("avgSNR",ctypes.c_double),
                ("lineFound",ctypes.c_int) ]
PFindConcentricEdgeReport=ctypes.POINTER(FindConcentricEdgeReport)
class CFindConcentricEdgeReport(ctypes_wrap.CStructWrapper):
    _struct=FindConcentricEdgeReport


class FindCircularEdgeReport(ctypes.Structure):
    _fields_=[  ("centerCalibrated",PointFloat),
                ("radiusCalibrated",ctypes.c_double),
                ("center",PointFloat),
                ("radius",ctypes.c_double),
                ("roundness",ctypes.c_double),
                ("avgStrength",ctypes.c_double),
                ("avgSNR",ctypes.c_double),
                ("circleFound",ctypes.c_int) ]
PFindCircularEdgeReport=ctypes.POINTER(FindCircularEdgeReport)
class CFindCircularEdgeReport(ctypes_wrap.CStructWrapper):
    _struct=FindCircularEdgeReport


class WindowSize(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_int),
                ("y",ctypes.c_int),
                ("stepSize",ctypes.c_int) ]
PWindowSize=ctypes.POINTER(WindowSize)
class CWindowSize(ctypes_wrap.CStructWrapper):
    _struct=WindowSize


class DisplacementVector(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_int),
                ("y",ctypes.c_int) ]
PDisplacementVector=ctypes.POINTER(DisplacementVector)
class CDisplacementVector(ctypes_wrap.CStructWrapper):
    _struct=DisplacementVector


class WaveletOptions(ctypes.Structure):
    _fields_=[  ("typeOfWavelet",ctypes.c_int),
                ("minEnergy",ctypes.c_float) ]
PWaveletOptions=ctypes.POINTER(WaveletOptions)
class CWaveletOptions(ctypes_wrap.CStructWrapper):
    _struct=WaveletOptions


class CooccurrenceOptions(ctypes.Structure):
    _fields_=[  ("level",ctypes.c_int),
                ("displacement",DisplacementVector) ]
PCooccurrenceOptions=ctypes.POINTER(CooccurrenceOptions)
class CCooccurrenceOptions(ctypes_wrap.CStructWrapper):
    _struct=CooccurrenceOptions


class ParticleClassifierLocalThresholdOptions(ctypes.Structure):
    _fields_=[  ("method",ctypes.c_int),
                ("particleType",ctypes.c_int),
                ("windowWidth",ctypes.c_uint),
                ("windowHeight",ctypes.c_uint),
                ("deviationWeight",ctypes.c_double) ]
PParticleClassifierLocalThresholdOptions=ctypes.POINTER(ParticleClassifierLocalThresholdOptions)
class CParticleClassifierLocalThresholdOptions(ctypes_wrap.CStructWrapper):
    _struct=ParticleClassifierLocalThresholdOptions


class RangeFloat(ctypes.Structure):
    _fields_=[  ("minValue",ctypes.c_float),
                ("maxValue",ctypes.c_float) ]
PRangeFloat=ctypes.POINTER(RangeFloat)
class CRangeFloat(ctypes_wrap.CStructWrapper):
    _struct=RangeFloat


class ParticleClassifierAutoThresholdOptions(ctypes.Structure):
    _fields_=[  ("method",ctypes.c_int),
                ("particleType",ctypes.c_int),
                ("limits",RangeFloat) ]
PParticleClassifierAutoThresholdOptions=ctypes.POINTER(ParticleClassifierAutoThresholdOptions)
class CParticleClassifierAutoThresholdOptions(ctypes_wrap.CStructWrapper):
    _struct=ParticleClassifierAutoThresholdOptions


class ParticleClassifierPreprocessingOptions2(ctypes.Structure):
    _fields_=[  ("thresholdType",ctypes.c_int),
                ("manualThresholdRange",RangeFloat),
                ("autoThresholdOptions",ParticleClassifierAutoThresholdOptions),
                ("localThresholdOptions",ParticleClassifierLocalThresholdOptions),
                ("rejectBorder",ctypes.c_int),
                ("numErosions",ctypes.c_int) ]
PParticleClassifierPreprocessingOptions2=ctypes.POINTER(ParticleClassifierPreprocessingOptions2)
class CParticleClassifierPreprocessingOptions2(ctypes_wrap.CStructWrapper):
    _struct=ParticleClassifierPreprocessingOptions2


class MeasureParticlesReport(ctypes.Structure):
    _fields_=[  ("pixelMeasurements",ctypes.POINTER(ctypes.POINTER(ctypes.c_double))),
                ("calibratedMeasurements",ctypes.POINTER(ctypes.POINTER(ctypes.c_double))),
                ("numParticles",ctypes.c_size_t),
                ("numMeasurements",ctypes.c_size_t) ]
PMeasureParticlesReport=ctypes.POINTER(MeasureParticlesReport)
class CMeasureParticlesReport(ctypes_wrap.CStructWrapper):
    _struct=MeasureParticlesReport


class GeometricPatternMatch3(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_float),
                ("scale",ctypes.c_float),
                ("score",ctypes.c_float),
                ("corner",PointFloat*4),
                ("inverse",ctypes.c_int),
                ("occlusion",ctypes.c_float),
                ("templateMatchCurveScore",ctypes.c_float),
                ("matchTemplateCurveScore",ctypes.c_float),
                ("correlationScore",ctypes.c_float),
                ("calibratedPosition",PointFloat),
                ("calibratedRotation",ctypes.c_float),
                ("calibratedCorner",PointFloat*4) ]
PGeometricPatternMatch3=ctypes.POINTER(GeometricPatternMatch3)
class CGeometricPatternMatch3(ctypes_wrap.CStructWrapper):
    _struct=GeometricPatternMatch3


class MatchGeometricPatternAdvancedOptions3(ctypes.Structure):
    _fields_=[  ("subpixelIterations",ctypes.c_uint),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_uint),
                ("targetTemplateCurveScore",ctypes.c_int),
                ("correlationScore",ctypes.c_int),
                ("minMatchSeparationDistance",ctypes.c_double),
                ("minMatchSeparationAngle",ctypes.c_double),
                ("minMatchSeparationScale",ctypes.c_double),
                ("maxMatchOverlap",ctypes.c_double),
                ("coarseResult",ctypes.c_int),
                ("enableCalibrationSupport",ctypes.c_int),
                ("enableContrastReversal",ctypes.c_int),
                ("matchStrategy",ctypes.c_int),
                ("refineMatchFactor",ctypes.c_uint),
                ("subpixelMatchFactor",ctypes.c_uint) ]
PMatchGeometricPatternAdvancedOptions3=ctypes.POINTER(MatchGeometricPatternAdvancedOptions3)
class CMatchGeometricPatternAdvancedOptions3(ctypes_wrap.CStructWrapper):
    _struct=MatchGeometricPatternAdvancedOptions3


class MatchGeometricPatternAdvancedOptions4(ctypes.Structure):
    _fields_=[  ("subpixelIterations",ctypes.c_uint),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_uint),
                ("targetTemplateCurveScore",ctypes.c_int),
                ("correlationScore",ctypes.c_int),
                ("minMatchSeparationDistance",ctypes.c_double),
                ("minMatchSeparationAngle",ctypes.c_double),
                ("minMatchSeparationScale",ctypes.c_double),
                ("maxMatchOverlap",ctypes.c_double),
                ("coarseResult",ctypes.c_int),
                ("enableCalibrationSupport",ctypes.c_int),
                ("enableContrastReversal",ctypes.c_int),
                ("matchStrategy",ctypes.c_int),
                ("refineMatchFactor",ctypes.c_uint),
                ("subpixelMatchFactor",ctypes.c_uint),
                ("contourMaxRefinements",ctypes.c_uint),
                ("scoringMethod",ctypes.c_uint),
                ("initialMatchAngularAccuracy",ctypes.c_uint) ]
PMatchGeometricPatternAdvancedOptions4=ctypes.POINTER(MatchGeometricPatternAdvancedOptions4)
class CMatchGeometricPatternAdvancedOptions4(ctypes_wrap.CStructWrapper):
    _struct=MatchGeometricPatternAdvancedOptions4


class MatchGeometricPatternAdvancedOptions5(ctypes.Structure):
    _fields_=[  ("subpixelIterations",ctypes.c_uint),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_uint),
                ("targetTemplateCurveScore",ctypes.c_int),
                ("correlationScore",ctypes.c_int),
                ("minMatchSeparationDistance",ctypes.c_double),
                ("minMatchSeparationAngle",ctypes.c_double),
                ("minMatchSeparationScale",ctypes.c_double),
                ("maxMatchOverlap",ctypes.c_double),
                ("coarseResult",ctypes.c_int),
                ("enableCalibrationSupport",ctypes.c_int),
                ("enableContrastReversal",ctypes.c_int),
                ("matchStrategy",ctypes.c_int),
                ("refineMatchFactor",ctypes.c_uint),
                ("subpixelMatchFactor",ctypes.c_uint),
                ("contourMaxRefinements",ctypes.c_uint),
                ("scoringMethod",ctypes.c_uint),
                ("initialMatchAngularAccuracy",ctypes.c_uint),
                ("enableDefectMap",ctypes.c_uint) ]
PMatchGeometricPatternAdvancedOptions5=ctypes.POINTER(MatchGeometricPatternAdvancedOptions5)
class CMatchGeometricPatternAdvancedOptions5(ctypes_wrap.CStructWrapper):
    _struct=MatchGeometricPatternAdvancedOptions5


class ColorOptions(ctypes.Structure):
    _fields_=[  ("colorClassificationResolution",ctypes.c_int),
                ("useLuminance",ctypes.c_uint),
                ("colorMode",ctypes.c_int) ]
PColorOptions=ctypes.POINTER(ColorOptions)
class CColorOptions(ctypes_wrap.CStructWrapper):
    _struct=ColorOptions


class SampleScore(ctypes.Structure):
    _fields_=[  ("className",ctypes.c_char_p),
                ("distance",ctypes.c_float),
                ("index",ctypes.c_uint) ]
PSampleScore=ctypes.POINTER(SampleScore)
class CSampleScore(ctypes_wrap.CStructWrapper):
    _struct=SampleScore


class ClassScore(ctypes.Structure):
    _fields_=[  ("className",ctypes.c_char_p),
                ("distance",ctypes.c_float) ]
PClassScore=ctypes.POINTER(ClassScore)
class CClassScore(ctypes_wrap.CStructWrapper):
    _struct=ClassScore


class ClassifierReportAdvanced(ctypes.Structure):
    _fields_=[  ("bestClassName",ctypes.c_char_p),
                ("classificationScore",ctypes.c_float),
                ("identificationScore",ctypes.c_float),
                ("allScores",ctypes.POINTER(ClassScore)),
                ("allScoresSize",ctypes.c_int),
                ("sampleScores",ctypes.POINTER(SampleScore)),
                ("sampleScoresSize",ctypes.c_int) ]
PClassifierReportAdvanced=ctypes.POINTER(ClassifierReportAdvanced)
class CClassifierReportAdvanced(ctypes_wrap.CStructWrapper):
    _struct=ClassifierReportAdvanced


class LearnGeometricPatternAdvancedOptions2(ctypes.Structure):
    _fields_=[  ("minScaleFactor",ctypes.c_double),
                ("maxScaleFactor",ctypes.c_double),
                ("minRotationAngleValue",ctypes.c_double),
                ("maxRotationAngleValue",ctypes.c_double),
                ("imageSamplingFactor",ctypes.c_uint) ]
PLearnGeometricPatternAdvancedOptions2=ctypes.POINTER(LearnGeometricPatternAdvancedOptions2)
class CLearnGeometricPatternAdvancedOptions2(ctypes_wrap.CStructWrapper):
    _struct=LearnGeometricPatternAdvancedOptions2


class ParticleFilterOptions2(ctypes.Structure):
    _fields_=[  ("rejectMatches",ctypes.c_int),
                ("rejectBorder",ctypes.c_int),
                ("fillHoles",ctypes.c_int),
                ("connectivity8",ctypes.c_int) ]
PParticleFilterOptions2=ctypes.POINTER(ParticleFilterOptions2)
class CParticleFilterOptions2(ctypes_wrap.CStructWrapper):
    _struct=ParticleFilterOptions2


class FindEdgeOptions2(ctypes.Structure):
    _fields_=[  ("direction",ctypes.c_int),
                ("showSearchArea",ctypes.c_int),
                ("showSearchLines",ctypes.c_int),
                ("showEdgesFound",ctypes.c_int),
                ("showResult",ctypes.c_int),
                ("searchAreaColor",RGBValue),
                ("searchLinesColor",RGBValue),
                ("searchEdgesColor",RGBValue),
                ("resultColor",RGBValue),
                ("overlayGroupName",ctypes.c_char_p),
                ("edgeOptions",EdgeOptions2) ]
PFindEdgeOptions2=ctypes.POINTER(FindEdgeOptions2)
class CFindEdgeOptions2(ctypes_wrap.CStructWrapper):
    _struct=FindEdgeOptions2


class EdgeInfo(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("calibratedPosition",PointFloat),
                ("distance",ctypes.c_double),
                ("calibratedDistance",ctypes.c_double),
                ("magnitude",ctypes.c_double),
                ("noisePeak",ctypes.c_double),
                ("rising",ctypes.c_int) ]
PEdgeInfo=ctypes.POINTER(EdgeInfo)
class CEdgeInfo(ctypes_wrap.CStructWrapper):
    _struct=EdgeInfo


class StraightEdge(ctypes.Structure):
    _fields_=[  ("straightEdgeCoordinates",LineFloat),
                ("calibratedStraightEdgeCoordinates",LineFloat),
                ("angle",ctypes.c_double),
                ("calibratedAngle",ctypes.c_double),
                ("score",ctypes.c_double),
                ("straightness",ctypes.c_double),
                ("averageSignalToNoiseRatio",ctypes.c_double),
                ("calibrationValid",ctypes.c_int),
                ("usedEdges",ctypes.POINTER(EdgeInfo)),
                ("numUsedEdges",ctypes.c_uint) ]
PStraightEdge=ctypes.POINTER(StraightEdge)
class CStraightEdge(ctypes_wrap.CStructWrapper):
    _struct=StraightEdge


class FindEdgeReport(ctypes.Structure):
    _fields_=[  ("straightEdges",ctypes.POINTER(StraightEdge)),
                ("numStraightEdges",ctypes.c_uint) ]
PFindEdgeReport=ctypes.POINTER(FindEdgeReport)
class CFindEdgeReport(ctypes_wrap.CStructWrapper):
    _struct=FindEdgeReport


class FindTransformRectOptions2(ctypes.Structure):
    _fields_=[  ("direction",ctypes.c_int),
                ("showSearchArea",ctypes.c_int),
                ("showSearchLines",ctypes.c_int),
                ("showEdgesFound",ctypes.c_int),
                ("showResult",ctypes.c_int),
                ("searchAreaColor",RGBValue),
                ("searchLinesColor",RGBValue),
                ("searchEdgesColor",RGBValue),
                ("resultColor",RGBValue),
                ("overlayGroupName",ctypes.c_char_p),
                ("edgeOptions",EdgeOptions2) ]
PFindTransformRectOptions2=ctypes.POINTER(FindTransformRectOptions2)
class CFindTransformRectOptions2(ctypes_wrap.CStructWrapper):
    _struct=FindTransformRectOptions2


class FindTransformRectsOptions2(ctypes.Structure):
    _fields_=[  ("direction",ctypes.c_int),
                ("showSearchArea",ctypes.c_int),
                ("showSearchLines",ctypes.c_int),
                ("showEdgesFound",ctypes.c_int),
                ("showResult",ctypes.c_int),
                ("searchAreaColor",RGBValue),
                ("searchLinesColor",RGBValue),
                ("searchEdgesColor",RGBValue),
                ("resultColor",RGBValue),
                ("overlayGroupName",ctypes.c_char_p),
                ("primaryEdgeOptions",EdgeOptions2),
                ("secondaryEdgeOptions",EdgeOptions2) ]
PFindTransformRectsOptions2=ctypes.POINTER(FindTransformRectsOptions2)
class CFindTransformRectsOptions2(ctypes_wrap.CStructWrapper):
    _struct=FindTransformRectsOptions2


class ReadTextReport3(ctypes.Structure):
    _fields_=[  ("readString",ctypes.c_char_p),
                ("characterReport",ctypes.POINTER(CharReport3)),
                ("numCharacterReports",ctypes.c_int),
                ("roiBoundingCharacters",ctypes.c_void_p) ]
PReadTextReport3=ctypes.POINTER(ReadTextReport3)
class CReadTextReport3(ctypes_wrap.CStructWrapper):
    _struct=ReadTextReport3


class ArcInfo2(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("radius",ctypes.c_double),
                ("startAngle",ctypes.c_double),
                ("endAngle",ctypes.c_double) ]
PArcInfo2=ctypes.POINTER(ArcInfo2)
class CArcInfo2(ctypes_wrap.CStructWrapper):
    _struct=ArcInfo2


class EdgeReport2(ctypes.Structure):
    _fields_=[  ("edges",ctypes.POINTER(EdgeInfo)),
                ("numEdges",ctypes.c_uint),
                ("gradientInfo",ctypes.POINTER(ctypes.c_double)),
                ("numGradientInfo",ctypes.c_uint),
                ("calibrationValid",ctypes.c_int) ]
PEdgeReport2=ctypes.POINTER(EdgeReport2)
class CEdgeReport2(ctypes_wrap.CStructWrapper):
    _struct=EdgeReport2


class SearchArcInfo(ctypes.Structure):
    _fields_=[  ("arcCoordinates",ArcInfo2),
                ("edgeReport",EdgeReport2) ]
PSearchArcInfo=ctypes.POINTER(SearchArcInfo)
class CSearchArcInfo(ctypes_wrap.CStructWrapper):
    _struct=SearchArcInfo


class ConcentricRakeReport2(ctypes.Structure):
    _fields_=[  ("firstEdges",ctypes.POINTER(EdgeInfo)),
                ("numFirstEdges",ctypes.c_uint),
                ("lastEdges",ctypes.POINTER(EdgeInfo)),
                ("numLastEdges",ctypes.c_uint),
                ("searchArcs",ctypes.POINTER(SearchArcInfo)),
                ("numSearchArcs",ctypes.c_uint) ]
PConcentricRakeReport2=ctypes.POINTER(ConcentricRakeReport2)
class CConcentricRakeReport2(ctypes_wrap.CStructWrapper):
    _struct=ConcentricRakeReport2


class SearchLineInfo(ctypes.Structure):
    _fields_=[  ("lineCoordinates",LineFloat),
                ("edgeReport",EdgeReport2) ]
PSearchLineInfo=ctypes.POINTER(SearchLineInfo)
class CSearchLineInfo(ctypes_wrap.CStructWrapper):
    _struct=SearchLineInfo


class SpokeReport2(ctypes.Structure):
    _fields_=[  ("firstEdges",ctypes.POINTER(EdgeInfo)),
                ("numFirstEdges",ctypes.c_uint),
                ("lastEdges",ctypes.POINTER(EdgeInfo)),
                ("numLastEdges",ctypes.c_uint),
                ("searchLines",ctypes.POINTER(SearchLineInfo)),
                ("numSearchLines",ctypes.c_uint) ]
PSpokeReport2=ctypes.POINTER(SpokeReport2)
class CSpokeReport2(ctypes_wrap.CStructWrapper):
    _struct=SpokeReport2


class RakeReport2(ctypes.Structure):
    _fields_=[  ("firstEdges",ctypes.POINTER(EdgeInfo)),
                ("numFirstEdges",ctypes.c_uint),
                ("lastEdges",ctypes.POINTER(EdgeInfo)),
                ("numLastEdges",ctypes.c_uint),
                ("searchLines",ctypes.POINTER(SearchLineInfo)),
                ("numSearchLines",ctypes.c_uint) ]
PRakeReport2=ctypes.POINTER(RakeReport2)
class CRakeReport2(ctypes_wrap.CStructWrapper):
    _struct=RakeReport2


class TransformBehaviors(ctypes.Structure):
    _fields_=[  ("ShiftBehavior",ctypes.c_int),
                ("ScaleBehavior",ctypes.c_int),
                ("RotateBehavior",ctypes.c_int),
                ("SymmetryBehavior",ctypes.c_int) ]
PTransformBehaviors=ctypes.POINTER(TransformBehaviors)
class CTransformBehaviors(ctypes_wrap.CStructWrapper):
    _struct=TransformBehaviors


class QRCodeDataToken(ctypes.Structure):
    _fields_=[  ("mode",ctypes.c_int),
                ("modeData",ctypes.c_uint),
                ("data",ctypes.POINTER(ctypes.c_ubyte)),
                ("dataLength",ctypes.c_uint) ]
PQRCodeDataToken=ctypes.POINTER(QRCodeDataToken)
class CQRCodeDataToken(ctypes_wrap.CStructWrapper):
    _struct=QRCodeDataToken


class ParticleFilterOptions(ctypes.Structure):
    _fields_=[  ("rejectMatches",ctypes.c_int),
                ("rejectBorder",ctypes.c_int),
                ("connectivity8",ctypes.c_int) ]
PParticleFilterOptions=ctypes.POINTER(ParticleFilterOptions)
class CParticleFilterOptions(ctypes_wrap.CStructWrapper):
    _struct=ParticleFilterOptions


class StraightEdgeReport2(ctypes.Structure):
    _fields_=[  ("straightEdges",ctypes.POINTER(StraightEdge)),
                ("numStraightEdges",ctypes.c_uint),
                ("searchLines",ctypes.POINTER(SearchLineInfo)),
                ("numSearchLines",ctypes.c_uint) ]
PStraightEdgeReport2=ctypes.POINTER(StraightEdgeReport2)
class CStraightEdgeReport2(ctypes_wrap.CStructWrapper):
    _struct=StraightEdgeReport2


class StraightEdgeOptions(ctypes.Structure):
    _fields_=[  ("numLines",ctypes.c_uint),
                ("searchMode",ctypes.c_int),
                ("minScore",ctypes.c_double),
                ("maxScore",ctypes.c_double),
                ("orientation",ctypes.c_double),
                ("angleRange",ctypes.c_double),
                ("angleTolerance",ctypes.c_double),
                ("stepSize",ctypes.c_uint),
                ("minSignalToNoiseRatio",ctypes.c_double),
                ("minCoverage",ctypes.c_double),
                ("houghIterations",ctypes.c_uint) ]
PStraightEdgeOptions=ctypes.POINTER(StraightEdgeOptions)
class CStraightEdgeOptions(ctypes_wrap.CStructWrapper):
    _struct=StraightEdgeOptions


class QRCodeSearchOptions(ctypes.Structure):
    _fields_=[  ("rotationMode",ctypes.c_int),
                ("skipLocation",ctypes.c_uint),
                ("edgeThreshold",ctypes.c_uint),
                ("demodulationMode",ctypes.c_int),
                ("cellSampleSize",ctypes.c_int),
                ("cellFilterMode",ctypes.c_int),
                ("skewDegreesAllowed",ctypes.c_uint) ]
PQRCodeSearchOptions=ctypes.POINTER(QRCodeSearchOptions)
class CQRCodeSearchOptions(ctypes_wrap.CStructWrapper):
    _struct=QRCodeSearchOptions


class QRCodeSizeOptions(ctypes.Structure):
    _fields_=[  ("minSize",ctypes.c_uint),
                ("maxSize",ctypes.c_uint) ]
PQRCodeSizeOptions=ctypes.POINTER(QRCodeSizeOptions)
class CQRCodeSizeOptions(ctypes_wrap.CStructWrapper):
    _struct=QRCodeSizeOptions


class QRCodeDescriptionOptions(ctypes.Structure):
    _fields_=[  ("dimensions",ctypes.c_int),
                ("polarity",ctypes.c_int),
                ("mirror",ctypes.c_int),
                ("modelType",ctypes.c_int) ]
PQRCodeDescriptionOptions=ctypes.POINTER(QRCodeDescriptionOptions)
class CQRCodeDescriptionOptions(ctypes_wrap.CStructWrapper):
    _struct=QRCodeDescriptionOptions


class QRCodeReport(ctypes.Structure):
    _fields_=[  ("found",ctypes.c_uint),
                ("data",ctypes.POINTER(ctypes.c_ubyte)),
                ("dataLength",ctypes.c_uint),
                ("boundingBox",PointFloat*4),
                ("tokenizedData",ctypes.POINTER(QRCodeDataToken)),
                ("sizeOfTokenizedData",ctypes.c_uint),
                ("numErrorsCorrected",ctypes.c_uint),
                ("dimensions",ctypes.c_uint),
                ("version",ctypes.c_uint),
                ("modelType",ctypes.c_int),
                ("streamMode",ctypes.c_int),
                ("matrixPolarity",ctypes.c_int),
                ("mirrored",ctypes.c_uint),
                ("positionInAppendStream",ctypes.c_uint),
                ("sizeOfAppendStream",ctypes.c_uint),
                ("firstEAN128ApplicationID",ctypes.c_int),
                ("firstECIDesignator",ctypes.c_int),
                ("appendStreamIdentifier",ctypes.c_uint),
                ("minimumEdgeStrength",ctypes.c_uint),
                ("demodulationMode",ctypes.c_int),
                ("cellSampleSize",ctypes.c_int),
                ("cellFilterMode",ctypes.c_int) ]
PQRCodeReport=ctypes.POINTER(QRCodeReport)
class CQRCodeReport(ctypes_wrap.CStructWrapper):
    _struct=QRCodeReport


class AIMGradeReport(ctypes.Structure):
    _fields_=[  ("overallGrade",ctypes.c_int),
                ("decodingGrade",ctypes.c_int),
                ("symbolContrastGrade",ctypes.c_int),
                ("symbolContrast",ctypes.c_float),
                ("printGrowthGrade",ctypes.c_int),
                ("printGrowth",ctypes.c_float),
                ("axialNonuniformityGrade",ctypes.c_int),
                ("axialNonuniformity",ctypes.c_float),
                ("unusedErrorCorrectionGrade",ctypes.c_int),
                ("unusedErrorCorrection",ctypes.c_float) ]
PAIMGradeReport=ctypes.POINTER(AIMGradeReport)
class CAIMGradeReport(ctypes_wrap.CStructWrapper):
    _struct=AIMGradeReport


class DataMatrixSizeOptions(ctypes.Structure):
    _fields_=[  ("minSize",ctypes.c_uint),
                ("maxSize",ctypes.c_uint),
                ("quietZoneWidth",ctypes.c_uint) ]
PDataMatrixSizeOptions=ctypes.POINTER(DataMatrixSizeOptions)
class CDataMatrixSizeOptions(ctypes_wrap.CStructWrapper):
    _struct=DataMatrixSizeOptions


class DataMatrixDescriptionOptions(ctypes.Structure):
    _fields_=[  ("aspectRatio",ctypes.c_float),
                ("rows",ctypes.c_uint),
                ("columns",ctypes.c_uint),
                ("rectangle",ctypes.c_int),
                ("ecc",ctypes.c_int),
                ("polarity",ctypes.c_int),
                ("cellFill",ctypes.c_int),
                ("minBorderIntegrity",ctypes.c_float),
                ("mirrorMode",ctypes.c_int) ]
PDataMatrixDescriptionOptions=ctypes.POINTER(DataMatrixDescriptionOptions)
class CDataMatrixDescriptionOptions(ctypes_wrap.CStructWrapper):
    _struct=DataMatrixDescriptionOptions


class DataMatrixSearchOptions(ctypes.Structure):
    _fields_=[  ("rotationMode",ctypes.c_int),
                ("skipLocation",ctypes.c_int),
                ("edgeThreshold",ctypes.c_uint),
                ("demodulationMode",ctypes.c_int),
                ("cellSampleSize",ctypes.c_int),
                ("cellFilterMode",ctypes.c_int),
                ("skewDegreesAllowed",ctypes.c_uint),
                ("maxIterations",ctypes.c_uint),
                ("initialSearchVectorWidth",ctypes.c_uint) ]
PDataMatrixSearchOptions=ctypes.POINTER(DataMatrixSearchOptions)
class CDataMatrixSearchOptions(ctypes_wrap.CStructWrapper):
    _struct=DataMatrixSearchOptions


class DataMatrixReport(ctypes.Structure):
    _fields_=[  ("found",ctypes.c_int),
                ("binary",ctypes.c_int),
                ("data",ctypes.POINTER(ctypes.c_ubyte)),
                ("dataLength",ctypes.c_uint),
                ("boundingBox",PointFloat*4),
                ("numErrorsCorrected",ctypes.c_uint),
                ("numErasuresCorrected",ctypes.c_uint),
                ("aspectRatio",ctypes.c_float),
                ("rows",ctypes.c_uint),
                ("columns",ctypes.c_uint),
                ("ecc",ctypes.c_int),
                ("polarity",ctypes.c_int),
                ("cellFill",ctypes.c_int),
                ("borderIntegrity",ctypes.c_float),
                ("mirrored",ctypes.c_int),
                ("minimumEdgeStrength",ctypes.c_uint),
                ("demodulationMode",ctypes.c_int),
                ("cellSampleSize",ctypes.c_int),
                ("cellFilterMode",ctypes.c_int),
                ("iterations",ctypes.c_uint) ]
PDataMatrixReport=ctypes.POINTER(DataMatrixReport)
class CDataMatrixReport(ctypes_wrap.CStructWrapper):
    _struct=DataMatrixReport


class JPEG2000FileAdvancedOptions(ctypes.Structure):
    _fields_=[  ("waveletMode",ctypes.c_int),
                ("useMultiComponentTransform",ctypes.c_int),
                ("maxWaveletTransformLevel",ctypes.c_uint),
                ("quantizationStepSize",ctypes.c_float) ]
PJPEG2000FileAdvancedOptions=ctypes.POINTER(JPEG2000FileAdvancedOptions)
class CJPEG2000FileAdvancedOptions(ctypes_wrap.CStructWrapper):
    _struct=JPEG2000FileAdvancedOptions


class MatchGeometricPatternAdvancedOptions2(ctypes.Structure):
    _fields_=[  ("minFeaturesUsed",ctypes.c_int),
                ("maxFeaturesUsed",ctypes.c_int),
                ("subpixelIterations",ctypes.c_int),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_int),
                ("matchTemplateCurveScore",ctypes.c_float),
                ("correlationScore",ctypes.c_int),
                ("minMatchSeparationDistance",ctypes.c_double),
                ("minMatchSeparationAngle",ctypes.c_double),
                ("minMatchSeparationScale",ctypes.c_double),
                ("maxMatchOverlap",ctypes.c_double),
                ("coarseResult",ctypes.c_int),
                ("smoothContours",ctypes.c_int),
                ("enableCalibrationSupport",ctypes.c_int) ]
PMatchGeometricPatternAdvancedOptions2=ctypes.POINTER(MatchGeometricPatternAdvancedOptions2)
class CMatchGeometricPatternAdvancedOptions2(ctypes_wrap.CStructWrapper):
    _struct=MatchGeometricPatternAdvancedOptions2


class InspectionAlignment(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_float),
                ("scale",ctypes.c_float) ]
PInspectionAlignment=ctypes.POINTER(InspectionAlignment)
class CInspectionAlignment(ctypes_wrap.CStructWrapper):
    _struct=InspectionAlignment


class InspectionOptions(ctypes.Structure):
    _fields_=[  ("registrationMethod",ctypes.c_int),
                ("normalizationMethod",ctypes.c_int),
                ("edgeThicknessToIgnore",ctypes.c_int),
                ("brightThreshold",ctypes.c_float),
                ("darkThreshold",ctypes.c_float),
                ("binary",ctypes.c_int) ]
PInspectionOptions=ctypes.POINTER(InspectionOptions)
class CInspectionOptions(ctypes_wrap.CStructWrapper):
    _struct=InspectionOptions


class CharReport2(ctypes.Structure):
    _fields_=[  ("character",ctypes.c_char_p),
                ("corner",PointFloat*4),
                ("lowThreshold",ctypes.c_int),
                ("highThreshold",ctypes.c_int),
                ("classificationScore",ctypes.c_int),
                ("verificationScore",ctypes.c_int),
                ("verified",ctypes.c_int) ]
PCharReport2=ctypes.POINTER(CharReport2)
class CCharReport2(ctypes_wrap.CStructWrapper):
    _struct=CharReport2


class CharInfo2(ctypes.Structure):
    _fields_=[  ("charValue",ctypes.c_char_p),
                ("charImage",ctypes.c_void_p),
                ("internalImage",ctypes.c_void_p),
                ("isReferenceChar",ctypes.c_int) ]
PCharInfo2=ctypes.POINTER(CharInfo2)
class CCharInfo2(ctypes_wrap.CStructWrapper):
    _struct=CharInfo2


class ReadTextReport2(ctypes.Structure):
    _fields_=[  ("readString",ctypes.c_char_p),
                ("characterReport",ctypes.POINTER(CharReport2)),
                ("numCharacterReports",ctypes.c_int) ]
PReadTextReport2=ctypes.POINTER(ReadTextReport2)
class CReadTextReport2(ctypes_wrap.CStructWrapper):
    _struct=ReadTextReport2


class EllipseFeature(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_double),
                ("minorRadius",ctypes.c_double),
                ("majorRadius",ctypes.c_double) ]
PEllipseFeature=ctypes.POINTER(EllipseFeature)
class CEllipseFeature(ctypes_wrap.CStructWrapper):
    _struct=EllipseFeature


class CircleFeature(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("radius",ctypes.c_double) ]
PCircleFeature=ctypes.POINTER(CircleFeature)
class CCircleFeature(ctypes_wrap.CStructWrapper):
    _struct=CircleFeature


class ConstCurveFeature(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("radius",ctypes.c_double),
                ("startAngle",ctypes.c_double),
                ("endAngle",ctypes.c_double) ]
PConstCurveFeature=ctypes.POINTER(ConstCurveFeature)
class CConstCurveFeature(ctypes_wrap.CStructWrapper):
    _struct=ConstCurveFeature


class RectangleFeature(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("corner",PointFloat*4),
                ("rotation",ctypes.c_double),
                ("width",ctypes.c_double),
                ("height",ctypes.c_double) ]
PRectangleFeature=ctypes.POINTER(RectangleFeature)
class CRectangleFeature(ctypes_wrap.CStructWrapper):
    _struct=RectangleFeature


class LegFeature(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("corner",PointFloat*4),
                ("rotation",ctypes.c_double),
                ("width",ctypes.c_double),
                ("height",ctypes.c_double) ]
PLegFeature=ctypes.POINTER(LegFeature)
class CLegFeature(ctypes_wrap.CStructWrapper):
    _struct=LegFeature


class CornerFeature(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_double),
                ("enclosedAngle",ctypes.c_double),
                ("isVirtual",ctypes.c_int) ]
PCornerFeature=ctypes.POINTER(CornerFeature)
class CCornerFeature(ctypes_wrap.CStructWrapper):
    _struct=CornerFeature


class LineFeature(ctypes.Structure):
    _fields_=[  ("startPoint",PointFloat),
                ("endPoint",PointFloat),
                ("length",ctypes.c_double),
                ("rotation",ctypes.c_double) ]
PLineFeature=ctypes.POINTER(LineFeature)
class CLineFeature(ctypes_wrap.CStructWrapper):
    _struct=LineFeature


class ParallelLinePairFeature(ctypes.Structure):
    _fields_=[  ("firstStartPoint",PointFloat),
                ("firstEndPoint",PointFloat),
                ("secondStartPoint",PointFloat),
                ("secondEndPoint",PointFloat),
                ("rotation",ctypes.c_double),
                ("distance",ctypes.c_double) ]
PParallelLinePairFeature=ctypes.POINTER(ParallelLinePairFeature)
class CParallelLinePairFeature(ctypes_wrap.CStructWrapper):
    _struct=ParallelLinePairFeature


class PairOfParallelLinePairsFeature(ctypes.Structure):
    _fields_=[  ("firstParallelLinePair",ParallelLinePairFeature),
                ("secondParallelLinePair",ParallelLinePairFeature),
                ("rotation",ctypes.c_double),
                ("distance",ctypes.c_double) ]
PPairOfParallelLinePairsFeature=ctypes.POINTER(PairOfParallelLinePairsFeature)
class CPairOfParallelLinePairsFeature(ctypes_wrap.CStructWrapper):
    _struct=PairOfParallelLinePairsFeature


class ClosedCurveFeature(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("arcLength",ctypes.c_double) ]
PClosedCurveFeature=ctypes.POINTER(ClosedCurveFeature)
class CClosedCurveFeature(ctypes_wrap.CStructWrapper):
    _struct=ClosedCurveFeature


class FeatureData(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("contourPoints",ctypes.POINTER(PointFloat)),
                ("numContourPoints",ctypes.c_int),
                ("feature",ctypes.c_void_p) ]
PFeatureData=ctypes.POINTER(FeatureData)
class CFeatureData(ctypes_wrap.CStructWrapper):
    _struct=FeatureData


class GeometricPatternMatch2(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_float),
                ("scale",ctypes.c_float),
                ("score",ctypes.c_float),
                ("corner",PointFloat*4),
                ("inverse",ctypes.c_int),
                ("occlusion",ctypes.c_float),
                ("templateMatchCurveScore",ctypes.c_float),
                ("matchTemplateCurveScore",ctypes.c_float),
                ("correlationScore",ctypes.c_float),
                ("label",String255),
                ("featureData",ctypes.POINTER(FeatureData)),
                ("numFeatureData",ctypes.c_int),
                ("calibratedPosition",PointFloat),
                ("calibratedRotation",ctypes.c_float),
                ("calibratedCorner",PointFloat*4) ]
PGeometricPatternMatch2=ctypes.POINTER(GeometricPatternMatch2)
class CGeometricPatternMatch2(ctypes_wrap.CStructWrapper):
    _struct=GeometricPatternMatch2


class LineMatch(ctypes.Structure):
    _fields_=[  ("startPoint",PointFloat),
                ("endPoint",PointFloat),
                ("length",ctypes.c_double),
                ("rotation",ctypes.c_double),
                ("score",ctypes.c_double) ]
PLineMatch=ctypes.POINTER(LineMatch)
class CLineMatch(ctypes_wrap.CStructWrapper):
    _struct=LineMatch


class LineDescriptor(ctypes.Structure):
    _fields_=[  ("minLength",ctypes.c_double),
                ("maxLength",ctypes.c_double) ]
PLineDescriptor=ctypes.POINTER(LineDescriptor)
class CLineDescriptor(ctypes_wrap.CStructWrapper):
    _struct=LineDescriptor


class RectangleDescriptor(ctypes.Structure):
    _fields_=[  ("minWidth",ctypes.c_double),
                ("maxWidth",ctypes.c_double),
                ("minHeight",ctypes.c_double),
                ("maxHeight",ctypes.c_double) ]
PRectangleDescriptor=ctypes.POINTER(RectangleDescriptor)
class CRectangleDescriptor(ctypes_wrap.CStructWrapper):
    _struct=RectangleDescriptor


class RectangleMatch(ctypes.Structure):
    _fields_=[  ("corner",PointFloat*4),
                ("rotation",ctypes.c_double),
                ("width",ctypes.c_double),
                ("height",ctypes.c_double),
                ("score",ctypes.c_double) ]
PRectangleMatch=ctypes.POINTER(RectangleMatch)
class CRectangleMatch(ctypes_wrap.CStructWrapper):
    _struct=RectangleMatch


class EllipseDescriptor(ctypes.Structure):
    _fields_=[  ("minMajorRadius",ctypes.c_double),
                ("maxMajorRadius",ctypes.c_double),
                ("minMinorRadius",ctypes.c_double),
                ("maxMinorRadius",ctypes.c_double) ]
PEllipseDescriptor=ctypes.POINTER(EllipseDescriptor)
class CEllipseDescriptor(ctypes_wrap.CStructWrapper):
    _struct=EllipseDescriptor


class EllipseMatch(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_double),
                ("majorRadius",ctypes.c_double),
                ("minorRadius",ctypes.c_double),
                ("score",ctypes.c_double) ]
PEllipseMatch=ctypes.POINTER(EllipseMatch)
class CEllipseMatch(ctypes_wrap.CStructWrapper):
    _struct=EllipseMatch


class CircleMatch(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("radius",ctypes.c_double),
                ("score",ctypes.c_double) ]
PCircleMatch=ctypes.POINTER(CircleMatch)
class CCircleMatch(ctypes_wrap.CStructWrapper):
    _struct=CircleMatch


class CircleDescriptor(ctypes.Structure):
    _fields_=[  ("minRadius",ctypes.c_double),
                ("maxRadius",ctypes.c_double) ]
PCircleDescriptor=ctypes.POINTER(CircleDescriptor)
class CCircleDescriptor(ctypes_wrap.CStructWrapper):
    _struct=CircleDescriptor


class ShapeDetectionOptions(ctypes.Structure):
    _fields_=[  ("mode",ctypes.c_uint),
                ("angleRanges",ctypes.POINTER(RangeFloat)),
                ("numAngleRanges",ctypes.c_int),
                ("scaleRange",RangeFloat),
                ("minMatchScore",ctypes.c_double) ]
PShapeDetectionOptions=ctypes.POINTER(ShapeDetectionOptions)
class CShapeDetectionOptions(ctypes_wrap.CStructWrapper):
    _struct=ShapeDetectionOptions


class Curve(ctypes.Structure):
    _fields_=[  ("points",ctypes.POINTER(PointFloat)),
                ("numPoints",ctypes.c_uint),
                ("closed",ctypes.c_int),
                ("curveLength",ctypes.c_double),
                ("minEdgeStrength",ctypes.c_double),
                ("maxEdgeStrength",ctypes.c_double),
                ("averageEdgeStrength",ctypes.c_double) ]
PCurve=ctypes.POINTER(Curve)
class CCurve(ctypes_wrap.CStructWrapper):
    _struct=Curve


class CurveOptions(ctypes.Structure):
    _fields_=[  ("extractionMode",ctypes.c_int),
                ("threshold",ctypes.c_int),
                ("filterSize",ctypes.c_int),
                ("minLength",ctypes.c_int),
                ("rowStepSize",ctypes.c_int),
                ("columnStepSize",ctypes.c_int),
                ("maxEndPointGap",ctypes.c_int),
                ("onlyClosed",ctypes.c_int),
                ("subpixelAccuracy",ctypes.c_int) ]
PCurveOptions=ctypes.POINTER(CurveOptions)
class CCurveOptions(ctypes_wrap.CStructWrapper):
    _struct=CurveOptions


class Barcode2DInfo(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("binary",ctypes.c_int),
                ("data",ctypes.POINTER(ctypes.c_ubyte)),
                ("dataLength",ctypes.c_uint),
                ("boundingBox",PointFloat*4),
                ("numErrorsCorrected",ctypes.c_uint),
                ("numErasuresCorrected",ctypes.c_uint),
                ("rows",ctypes.c_uint),
                ("columns",ctypes.c_uint) ]
PBarcode2DInfo=ctypes.POINTER(Barcode2DInfo)
class CBarcode2DInfo(ctypes_wrap.CStructWrapper):
    _struct=Barcode2DInfo


class DataMatrixOptions(ctypes.Structure):
    _fields_=[  ("searchMode",ctypes.c_int),
                ("contrast",ctypes.c_int),
                ("cellShape",ctypes.c_int),
                ("barcodeShape",ctypes.c_int),
                ("subtype",ctypes.c_int) ]
PDataMatrixOptions=ctypes.POINTER(DataMatrixOptions)
class CDataMatrixOptions(ctypes_wrap.CStructWrapper):
    _struct=DataMatrixOptions


class ClassifierAccuracyReport(ctypes.Structure):
    _fields_=[  ("size",ctypes.c_int),
                ("accuracy",ctypes.c_float),
                ("classNames",ctypes.POINTER(ctypes.c_char_p)),
                ("classAccuracy",ctypes.POINTER(ctypes.c_double)),
                ("classPredictiveValue",ctypes.POINTER(ctypes.c_double)),
                ("classificationDistribution",ctypes.POINTER(ctypes.POINTER(ctypes.c_int))) ]
PClassifierAccuracyReport=ctypes.POINTER(ClassifierAccuracyReport)
class CClassifierAccuracyReport(ctypes_wrap.CStructWrapper):
    _struct=ClassifierAccuracyReport


class NearestNeighborClassResult(ctypes.Structure):
    _fields_=[  ("className",ctypes.c_char_p),
                ("standardDeviation",ctypes.c_float),
                ("count",ctypes.c_int) ]
PNearestNeighborClassResult=ctypes.POINTER(NearestNeighborClassResult)
class CNearestNeighborClassResult(ctypes_wrap.CStructWrapper):
    _struct=NearestNeighborClassResult


class NearestNeighborTrainingReport(ctypes.Structure):
    _fields_=[  ("classDistancesTable",ctypes.POINTER(ctypes.POINTER(ctypes.c_float))),
                ("allScores",ctypes.POINTER(NearestNeighborClassResult)),
                ("allScoresSize",ctypes.c_int) ]
PNearestNeighborTrainingReport=ctypes.POINTER(NearestNeighborTrainingReport)
class CNearestNeighborTrainingReport(ctypes_wrap.CStructWrapper):
    _struct=NearestNeighborTrainingReport


class ParticleClassifierPreprocessingOptions(ctypes.Structure):
    _fields_=[  ("manualThreshold",ctypes.c_int),
                ("manualThresholdRange",RangeFloat),
                ("autoThresholdMethod",ctypes.c_int),
                ("limits",RangeFloat),
                ("particleType",ctypes.c_int),
                ("rejectBorder",ctypes.c_int),
                ("numErosions",ctypes.c_int) ]
PParticleClassifierPreprocessingOptions=ctypes.POINTER(ParticleClassifierPreprocessingOptions)
class CParticleClassifierPreprocessingOptions(ctypes_wrap.CStructWrapper):
    _struct=ParticleClassifierPreprocessingOptions


class ClassifierSampleInfo(ctypes.Structure):
    _fields_=[  ("className",ctypes.c_char_p),
                ("featureVector",ctypes.POINTER(ctypes.c_double)),
                ("featureVectorSize",ctypes.c_int),
                ("thumbnail",ctypes.c_void_p) ]
PClassifierSampleInfo=ctypes.POINTER(ClassifierSampleInfo)
class CClassifierSampleInfo(ctypes_wrap.CStructWrapper):
    _struct=ClassifierSampleInfo


class ClassifierReport(ctypes.Structure):
    _fields_=[  ("bestClassName",ctypes.c_char_p),
                ("classificationScore",ctypes.c_float),
                ("identificationScore",ctypes.c_float),
                ("allScores",ctypes.POINTER(ClassScore)),
                ("allScoresSize",ctypes.c_int) ]
PClassifierReport=ctypes.POINTER(ClassifierReport)
class CClassifierReport(ctypes_wrap.CStructWrapper):
    _struct=ClassifierReport


class NearestNeighborOptions(ctypes.Structure):
    _fields_=[  ("method",ctypes.c_int),
                ("metric",ctypes.c_int),
                ("k",ctypes.c_int) ]
PNearestNeighborOptions=ctypes.POINTER(NearestNeighborOptions)
class CNearestNeighborOptions(ctypes_wrap.CStructWrapper):
    _struct=NearestNeighborOptions


class ParticleClassifierOptions(ctypes.Structure):
    _fields_=[  ("scaleDependence",ctypes.c_float),
                ("mirrorDependence",ctypes.c_float) ]
PParticleClassifierOptions=ctypes.POINTER(ParticleClassifierOptions)
class CParticleClassifierOptions(ctypes_wrap.CStructWrapper):
    _struct=ParticleClassifierOptions


class RGBU64Value(ctypes.Structure):
    _fields_=[  ("B",ctypes.c_ushort),
                ("G",ctypes.c_ushort),
                ("R",ctypes.c_ushort),
                ("alpha",ctypes.c_ushort) ]
PRGBU64Value=ctypes.POINTER(RGBU64Value)
class CRGBU64Value(ctypes_wrap.CStructWrapper):
    _struct=RGBU64Value


class GeometricPatternMatch(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_float),
                ("scale",ctypes.c_float),
                ("score",ctypes.c_float),
                ("corner",PointFloat*4),
                ("inverse",ctypes.c_int),
                ("occlusion",ctypes.c_float),
                ("templateMatchCurveScore",ctypes.c_float),
                ("matchTemplateCurveScore",ctypes.c_float),
                ("correlationScore",ctypes.c_float) ]
PGeometricPatternMatch=ctypes.POINTER(GeometricPatternMatch)
class CGeometricPatternMatch(ctypes_wrap.CStructWrapper):
    _struct=GeometricPatternMatch


class MatchGeometricPatternAdvancedOptions(ctypes.Structure):
    _fields_=[  ("minFeaturesUsed",ctypes.c_int),
                ("maxFeaturesUsed",ctypes.c_int),
                ("subpixelIterations",ctypes.c_int),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_int),
                ("matchTemplateCurveScore",ctypes.c_int),
                ("correlationScore",ctypes.c_int),
                ("minMatchSeparationDistance",ctypes.c_double),
                ("minMatchSeparationAngle",ctypes.c_double),
                ("minMatchSeparationScale",ctypes.c_double),
                ("maxMatchOverlap",ctypes.c_double),
                ("coarseResult",ctypes.c_int) ]
PMatchGeometricPatternAdvancedOptions=ctypes.POINTER(MatchGeometricPatternAdvancedOptions)
class CMatchGeometricPatternAdvancedOptions(ctypes_wrap.CStructWrapper):
    _struct=MatchGeometricPatternAdvancedOptions


class MatchGeometricPatternOptions(ctypes.Structure):
    _fields_=[  ("mode",ctypes.c_uint),
                ("subpixelAccuracy",ctypes.c_int),
                ("angleRanges",ctypes.POINTER(RangeFloat)),
                ("numAngleRanges",ctypes.c_int),
                ("scaleRange",RangeFloat),
                ("occlusionRange",RangeFloat),
                ("numMatchesRequested",ctypes.c_int),
                ("minMatchScore",ctypes.c_float) ]
PMatchGeometricPatternOptions=ctypes.POINTER(MatchGeometricPatternOptions)
class CMatchGeometricPatternOptions(ctypes_wrap.CStructWrapper):
    _struct=MatchGeometricPatternOptions


class LearnGeometricPatternAdvancedOptions(ctypes.Structure):
    _fields_=[  ("minRectLength",ctypes.c_int),
                ("minRectAspectRatio",ctypes.c_double),
                ("minRadius",ctypes.c_int),
                ("minLineLength",ctypes.c_int),
                ("minFeatureStrength",ctypes.c_double),
                ("maxFeaturesUsed",ctypes.c_int),
                ("maxPixelDistanceFromLine",ctypes.c_int) ]
PLearnGeometricPatternAdvancedOptions=ctypes.POINTER(LearnGeometricPatternAdvancedOptions)
class CLearnGeometricPatternAdvancedOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnGeometricPatternAdvancedOptions


class FitEllipseOptions(ctypes.Structure):
    _fields_=[  ("rejectOutliers",ctypes.c_int),
                ("minScore",ctypes.c_double),
                ("pixelRadius",ctypes.c_double),
                ("maxIterations",ctypes.c_int) ]
PFitEllipseOptions=ctypes.POINTER(FitEllipseOptions)
class CFitEllipseOptions(ctypes_wrap.CStructWrapper):
    _struct=FitEllipseOptions


class FitCircleOptions(ctypes.Structure):
    _fields_=[  ("rejectOutliers",ctypes.c_int),
                ("minScore",ctypes.c_double),
                ("pixelRadius",ctypes.c_double),
                ("maxIterations",ctypes.c_int) ]
PFitCircleOptions=ctypes.POINTER(FitCircleOptions)
class CFitCircleOptions(ctypes_wrap.CStructWrapper):
    _struct=FitCircleOptions


class ConstructROIOptions2(ctypes.Structure):
    _fields_=[  ("windowNumber",ctypes.c_int),
                ("windowTitle",ctypes.c_char_p),
                ("type",ctypes.c_int),
                ("palette",ctypes.POINTER(RGBValue)),
                ("numColors",ctypes.c_int),
                ("maxContours",ctypes.c_uint) ]
PConstructROIOptions2=ctypes.POINTER(ConstructROIOptions2)
class CConstructROIOptions2(ctypes_wrap.CStructWrapper):
    _struct=ConstructROIOptions2


class HSLValue(ctypes.Structure):
    _fields_=[  ("L",ctypes.c_ubyte),
                ("S",ctypes.c_ubyte),
                ("H",ctypes.c_ubyte),
                ("alpha",ctypes.c_ubyte) ]
PHSLValue=ctypes.POINTER(HSLValue)
class CHSLValue(ctypes_wrap.CStructWrapper):
    _struct=HSLValue


class HSVValue(ctypes.Structure):
    _fields_=[  ("V",ctypes.c_ubyte),
                ("S",ctypes.c_ubyte),
                ("H",ctypes.c_ubyte),
                ("alpha",ctypes.c_ubyte) ]
PHSVValue=ctypes.POINTER(HSVValue)
class CHSVValue(ctypes_wrap.CStructWrapper):
    _struct=HSVValue


class HSIValue(ctypes.Structure):
    _fields_=[  ("I",ctypes.c_ubyte),
                ("S",ctypes.c_ubyte),
                ("H",ctypes.c_ubyte),
                ("alpha",ctypes.c_ubyte) ]
PHSIValue=ctypes.POINTER(HSIValue)
class CHSIValue(ctypes_wrap.CStructWrapper):
    _struct=HSIValue


class CIELabValue(ctypes.Structure):
    _fields_=[  ("b",ctypes.c_double),
                ("a",ctypes.c_double),
                ("L",ctypes.c_double),
                ("alpha",ctypes.c_ubyte) ]
PCIELabValue=ctypes.POINTER(CIELabValue)
class CCIELabValue(ctypes_wrap.CStructWrapper):
    _struct=CIELabValue


class CIEXYZValue(ctypes.Structure):
    _fields_=[  ("Z",ctypes.c_double),
                ("Y",ctypes.c_double),
                ("X",ctypes.c_double),
                ("alpha",ctypes.c_ubyte) ]
PCIEXYZValue=ctypes.POINTER(CIEXYZValue)
class CCIEXYZValue(ctypes_wrap.CStructWrapper):
    _struct=CIEXYZValue


class BestEllipse2(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("majorAxisStart",PointFloat),
                ("majorAxisEnd",PointFloat),
                ("minorAxisStart",PointFloat),
                ("minorAxisEnd",PointFloat),
                ("area",ctypes.c_double),
                ("perimeter",ctypes.c_double),
                ("error",ctypes.c_double),
                ("valid",ctypes.c_int),
                ("pointsUsed",ctypes.POINTER(ctypes.c_int)),
                ("numPointsUsed",ctypes.c_int) ]
PBestEllipse2=ctypes.POINTER(BestEllipse2)
class CBestEllipse2(ctypes_wrap.CStructWrapper):
    _struct=BestEllipse2


class LearnPatternAdvancedShiftOptions(ctypes.Structure):
    _fields_=[  ("initialStepSize",ctypes.c_int),
                ("initialSampleSize",ctypes.c_int),
                ("initialSampleSizeFactor",ctypes.c_double),
                ("finalSampleSize",ctypes.c_int),
                ("finalSampleSizeFactor",ctypes.c_double),
                ("subpixelSampleSize",ctypes.c_int),
                ("subpixelSampleSizeFactor",ctypes.c_double) ]
PLearnPatternAdvancedShiftOptions=ctypes.POINTER(LearnPatternAdvancedShiftOptions)
class CLearnPatternAdvancedShiftOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnPatternAdvancedShiftOptions


class LearnPatternAdvancedRotationOptions(ctypes.Structure):
    _fields_=[  ("searchStrategySupport",ctypes.c_int),
                ("initialStepSize",ctypes.c_int),
                ("initialSampleSize",ctypes.c_int),
                ("initialSampleSizeFactor",ctypes.c_double),
                ("initialAngularAccuracy",ctypes.c_int),
                ("finalSampleSize",ctypes.c_int),
                ("finalSampleSizeFactor",ctypes.c_double),
                ("finalAngularAccuracy",ctypes.c_int),
                ("subpixelSampleSize",ctypes.c_int),
                ("subpixelSampleSizeFactor",ctypes.c_double) ]
PLearnPatternAdvancedRotationOptions=ctypes.POINTER(LearnPatternAdvancedRotationOptions)
class CLearnPatternAdvancedRotationOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnPatternAdvancedRotationOptions


class LearnPatternAdvancedOptions(ctypes.Structure):
    _fields_=[  ("shiftOptions",ctypes.POINTER(LearnPatternAdvancedShiftOptions)),
                ("rotationOptions",ctypes.POINTER(LearnPatternAdvancedRotationOptions)) ]
PLearnPatternAdvancedOptions=ctypes.POINTER(LearnPatternAdvancedOptions)
class CLearnPatternAdvancedOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnPatternAdvancedOptions


class AVIInfo(ctypes.Structure):
    _fields_=[  ("width",ctypes.c_uint),
                ("height",ctypes.c_uint),
                ("imageType",ctypes.c_int),
                ("numFrames",ctypes.c_uint),
                ("framesPerSecond",ctypes.c_uint),
                ("filterName",ctypes.c_char_p),
                ("hasData",ctypes.c_int),
                ("maxDataSize",ctypes.c_uint) ]
PAVIInfo=ctypes.POINTER(AVIInfo)
class CAVIInfo(ctypes_wrap.CStructWrapper):
    _struct=AVIInfo


class CodecSourceType(enum.IntEnum):
    AVI_DEFAULT_CODEC                =_int32(0)
    AVI_VFW_CODEC                    =_int32(1)
    AVI_FFMPEG_CODEC                 =_int32(2)
    IMAQ_CODEC_SOURCE_TYPE_SIZE_GUARD=_int32(0xFFFFFFFF)
dCodecSourceType={a.name:a.value for a in CodecSourceType}
drCodecSourceType={a.value:a.name for a in CodecSourceType}


class LearnPatternAdvancedLDOptions(ctypes.Structure):
    _fields_=[  ("searchStrategySupport",ctypes.c_int),
                ("initialStepSize",ctypes.c_int),
                ("initialSampleSize",ctypes.c_int),
                ("initialSampleSizeFactor",ctypes.c_double),
                ("initialAngularAccuracy",ctypes.c_int),
                ("finalSampleSize",ctypes.c_int),
                ("finalSampleSizeFactor",ctypes.c_double),
                ("finalAngularAccuracy",ctypes.c_int),
                ("subpixelSampleSize",ctypes.c_int),
                ("subpixelSampleSizeFactor",ctypes.c_double) ]
PLearnPatternAdvancedLDOptions=ctypes.POINTER(LearnPatternAdvancedLDOptions)
class CLearnPatternAdvancedLDOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnPatternAdvancedLDOptions


class LearnPatternAdvancedPyramidOptions(ctypes.Structure):
    _fields_=[  ("subpixelSampleSize",ctypes.c_int),
                ("subpixelSampleSizeFactor",ctypes.c_double) ]
PLearnPatternAdvancedPyramidOptions=ctypes.POINTER(LearnPatternAdvancedPyramidOptions)
class CLearnPatternAdvancedPyramidOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnPatternAdvancedPyramidOptions


class MatchPatternAdvancedOptions(ctypes.Structure):
    _fields_=[  ("subpixelIterations",ctypes.c_int),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_int),
                ("matchListReductionFactor",ctypes.c_int),
                ("initialStepSize",ctypes.c_int),
                ("searchStrategy",ctypes.c_int),
                ("intermediateAngularAccuracy",ctypes.c_int) ]
PMatchPatternAdvancedOptions=ctypes.POINTER(MatchPatternAdvancedOptions)
class CMatchPatternAdvancedOptions(ctypes_wrap.CStructWrapper):
    _struct=MatchPatternAdvancedOptions


class MatchPatternAdvancedOptionsLD(ctypes.Structure):
    _fields_=[  ("subpixelIterations",ctypes.c_int),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_int),
                ("matchListReductionFactor",ctypes.c_int),
                ("initialStepSize",ctypes.c_int),
                ("searchStrategy",ctypes.c_int),
                ("intermediateAngularAccuracy",ctypes.c_int) ]
PMatchPatternAdvancedOptionsLD=ctypes.POINTER(MatchPatternAdvancedOptionsLD)
class CMatchPatternAdvancedOptionsLD(ctypes_wrap.CStructWrapper):
    _struct=MatchPatternAdvancedOptionsLD


class MatchPatternAdvancedOptionsPyramid(ctypes.Structure):
    _fields_=[  ("maxPyramidLevel",ctypes.c_int),
                ("enableSpiralSearch",ctypes.c_int),
                ("enableSubpixelSearch",ctypes.c_int),
                ("subpixelIterations",ctypes.c_int),
                ("subpixelTolerance",ctypes.c_double),
                ("initialMatchListLength",ctypes.c_int),
                ("matchListReductionFactor",ctypes.c_int),
                ("initialAngularAccuracy",ctypes.c_int),
                ("processBorderMatches",ctypes.c_int),
                ("fastMatchMode",ctypes.c_int) ]
PMatchPatternAdvancedOptionsPyramid=ctypes.POINTER(MatchPatternAdvancedOptionsPyramid)
class CMatchPatternAdvancedOptionsPyramid(ctypes_wrap.CStructWrapper):
    _struct=MatchPatternAdvancedOptionsPyramid


class ParticleFilterCriteria2(ctypes.Structure):
    _fields_=[  ("parameter",ctypes.c_int),
                ("lower",ctypes.c_float),
                ("upper",ctypes.c_float),
                ("calibrated",ctypes.c_int),
                ("exclude",ctypes.c_int) ]
PParticleFilterCriteria2=ctypes.POINTER(ParticleFilterCriteria2)
class CParticleFilterCriteria2(ctypes_wrap.CStructWrapper):
    _struct=ParticleFilterCriteria2


class BestCircle2(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("radius",ctypes.c_double),
                ("area",ctypes.c_double),
                ("perimeter",ctypes.c_double),
                ("error",ctypes.c_double),
                ("valid",ctypes.c_int),
                ("pointsUsed",ctypes.POINTER(ctypes.c_int)),
                ("numPointsUsed",ctypes.c_int) ]
PBestCircle2=ctypes.POINTER(BestCircle2)
class CBestCircle2(ctypes_wrap.CStructWrapper):
    _struct=BestCircle2


class OCRSpacingOptions(ctypes.Structure):
    _fields_=[  ("minCharSpacing",ctypes.c_int),
                ("minCharSize",ctypes.c_int),
                ("maxCharSize",ctypes.c_int),
                ("maxHorizontalElementSpacing",ctypes.c_int),
                ("maxVerticalElementSpacing",ctypes.c_int),
                ("minBoundingRectWidth",ctypes.c_int),
                ("maxBoundingRectWidth",ctypes.c_int),
                ("minBoundingRectHeight",ctypes.c_int),
                ("maxBoundingRectHeight",ctypes.c_int),
                ("autoSplit",ctypes.c_int) ]
POCRSpacingOptions=ctypes.POINTER(OCRSpacingOptions)
class COCRSpacingOptions(ctypes_wrap.CStructWrapper):
    _struct=OCRSpacingOptions


class OCRProcessingOptions(ctypes.Structure):
    _fields_=[  ("mode",ctypes.c_int),
                ("lowThreshold",ctypes.c_int),
                ("highThreshold",ctypes.c_int),
                ("blockCount",ctypes.c_int),
                ("fastThreshold",ctypes.c_int),
                ("biModalCalculation",ctypes.c_int),
                ("darkCharacters",ctypes.c_int),
                ("removeParticlesTouchingROI",ctypes.c_int),
                ("erosionCount",ctypes.c_int) ]
POCRProcessingOptions=ctypes.POINTER(OCRProcessingOptions)
class COCRProcessingOptions(ctypes_wrap.CStructWrapper):
    _struct=OCRProcessingOptions


class ReadTextOptions(ctypes.Structure):
    _fields_=[  ("validChars",String255*255),
                ("numValidChars",ctypes.c_int),
                ("substitutionChar",ctypes.c_char),
                ("readStrategy",ctypes.c_int),
                ("acceptanceLevel",ctypes.c_int),
                ("aspectRatio",ctypes.c_int),
                ("readResolution",ctypes.c_int) ]
PReadTextOptions=ctypes.POINTER(ReadTextOptions)
class CReadTextOptions(ctypes_wrap.CStructWrapper):
    _struct=ReadTextOptions


class CharInfo(ctypes.Structure):
    _fields_=[  ("charValue",ctypes.c_char_p),
                ("charImage",ctypes.c_void_p),
                ("internalImage",ctypes.c_void_p) ]
PCharInfo=ctypes.POINTER(CharInfo)
class CCharInfo(ctypes_wrap.CStructWrapper):
    _struct=CharInfo


class Rect(ctypes.Structure):
    _fields_=[  ("top",ctypes.c_int),
                ("left",ctypes.c_int),
                ("height",ctypes.c_int),
                ("width",ctypes.c_int) ]
PRect=ctypes.POINTER(Rect)
class CRect(ctypes_wrap.CStructWrapper):
    _struct=Rect


class CharReport(ctypes.Structure):
    _fields_=[  ("character",ctypes.c_char_p),
                ("corner",PointFloat*4),
                ("reserved",ctypes.c_int),
                ("lowThreshold",ctypes.c_int),
                ("highThreshold",ctypes.c_int) ]
PCharReport=ctypes.POINTER(CharReport)
class CCharReport(ctypes_wrap.CStructWrapper):
    _struct=CharReport


class ReadTextReport(ctypes.Structure):
    _fields_=[  ("readString",ctypes.c_char_p),
                ("characterReport",ctypes.POINTER(CharReport)),
                ("numCharacterReports",ctypes.c_int) ]
PReadTextReport=ctypes.POINTER(ReadTextReport)
class CReadTextReport(ctypes_wrap.CStructWrapper):
    _struct=ReadTextReport


class Point(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_int),
                ("y",ctypes.c_int) ]
PPoint=ctypes.POINTER(Point)
class CPoint(ctypes_wrap.CStructWrapper):
    _struct=Point


class Annulus(ctypes.Structure):
    _fields_=[  ("center",Point),
                ("innerRadius",ctypes.c_int),
                ("outerRadius",ctypes.c_int),
                ("startAngle",ctypes.c_double),
                ("endAngle",ctypes.c_double) ]
PAnnulus=ctypes.POINTER(Annulus)
class CAnnulus(ctypes_wrap.CStructWrapper):
    _struct=Annulus


class EdgeLocationReport(ctypes.Structure):
    _fields_=[  ("edges",ctypes.POINTER(PointFloat)),
                ("numEdges",ctypes.c_int) ]
PEdgeLocationReport=ctypes.POINTER(EdgeLocationReport)
class CEdgeLocationReport(ctypes_wrap.CStructWrapper):
    _struct=EdgeLocationReport


class EdgeOptions(ctypes.Structure):
    _fields_=[  ("threshold",ctypes.c_uint),
                ("width",ctypes.c_uint),
                ("steepness",ctypes.c_uint),
                ("subpixelType",ctypes.c_int),
                ("subpixelDivisions",ctypes.c_uint) ]
PEdgeOptions=ctypes.POINTER(EdgeOptions)
class CEdgeOptions(ctypes_wrap.CStructWrapper):
    _struct=EdgeOptions


class EdgeReport(ctypes.Structure):
    _fields_=[  ("location",ctypes.c_float),
                ("contrast",ctypes.c_float),
                ("polarity",ctypes.c_int),
                ("reserved",ctypes.c_float),
                ("coordinate",PointFloat) ]
PEdgeReport=ctypes.POINTER(EdgeReport)
class CEdgeReport(ctypes_wrap.CStructWrapper):
    _struct=EdgeReport


class ExtremeReport(ctypes.Structure):
    _fields_=[  ("location",ctypes.c_double),
                ("amplitude",ctypes.c_double),
                ("secondDerivative",ctypes.c_double) ]
PExtremeReport=ctypes.POINTER(ExtremeReport)
class CExtremeReport(ctypes_wrap.CStructWrapper):
    _struct=ExtremeReport


class FitLineOptions(ctypes.Structure):
    _fields_=[  ("minScore",ctypes.c_float),
                ("pixelRadius",ctypes.c_float),
                ("numRefinements",ctypes.c_int) ]
PFitLineOptions=ctypes.POINTER(FitLineOptions)
class CFitLineOptions(ctypes_wrap.CStructWrapper):
    _struct=FitLineOptions


class DisplayMapping(ctypes.Structure):
    _fields_=[  ("method",ctypes.c_int),
                ("minimumValue",ctypes.c_int),
                ("maximumValue",ctypes.c_int),
                ("shiftCount",ctypes.c_int) ]
PDisplayMapping=ctypes.POINTER(DisplayMapping)
class CDisplayMapping(ctypes_wrap.CStructWrapper):
    _struct=DisplayMapping


class DetectExtremesOptions(ctypes.Structure):
    _fields_=[  ("threshold",ctypes.c_double),
                ("width",ctypes.c_int) ]
PDetectExtremesOptions=ctypes.POINTER(DetectExtremesOptions)
class CDetectExtremesOptions(ctypes_wrap.CStructWrapper):
    _struct=DetectExtremesOptions


class ImageInfo(ctypes.Structure):
    _fields_=[  ("imageUnit",ctypes.c_int),
                ("stepX",ctypes.c_float),
                ("stepY",ctypes.c_float),
                ("imageType",ctypes.c_int),
                ("xRes",ctypes.c_int),
                ("yRes",ctypes.c_int),
                ("xOffset",ctypes.c_int),
                ("yOffset",ctypes.c_int),
                ("border",ctypes.c_int),
                ("pixelsPerLine",ctypes.c_int),
                ("reserved0",ctypes.c_void_p),
                ("reserved1",ctypes.c_void_p),
                ("imageStart",ctypes.c_void_p) ]
PImageInfo=ctypes.POINTER(ImageInfo)
class CImageInfo(ctypes_wrap.CStructWrapper):
    _struct=ImageInfo


class LCDOptions(ctypes.Structure):
    _fields_=[  ("litSegments",ctypes.c_int),
                ("threshold",ctypes.c_float),
                ("sign",ctypes.c_int),
                ("decimalPoint",ctypes.c_int) ]
PLCDOptions=ctypes.POINTER(LCDOptions)
class CLCDOptions(ctypes_wrap.CStructWrapper):
    _struct=LCDOptions


class LCDSegments(ctypes.Structure):
    _fields_=[  ("a",ctypes.c_uint),
                ("b",ctypes.c_uint),
                ("c",ctypes.c_uint),
                ("d",ctypes.c_uint),
                ("e",ctypes.c_uint),
                ("f",ctypes.c_uint),
                ("g",ctypes.c_uint),
                ("reserved",ctypes.c_uint) ]
PLCDSegments=ctypes.POINTER(LCDSegments)
class CLCDSegments(ctypes_wrap.CStructWrapper):
    _struct=LCDSegments


class LCDReport(ctypes.Structure):
    _fields_=[  ("text",ctypes.c_char_p),
                ("segmentInfo",ctypes.POINTER(LCDSegments)),
                ("numCharacters",ctypes.c_int),
                ("reserved",ctypes.c_int) ]
PLCDReport=ctypes.POINTER(LCDReport)
class CLCDReport(ctypes_wrap.CStructWrapper):
    _struct=LCDReport


class LearnCalibrationOptions(ctypes.Structure):
    _fields_=[  ("mode",ctypes.c_int),
                ("method",ctypes.c_int),
                ("roi",ctypes.c_int),
                ("learnMap",ctypes.c_int),
                ("learnTable",ctypes.c_int) ]
PLearnCalibrationOptions=ctypes.POINTER(LearnCalibrationOptions)
class CLearnCalibrationOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnCalibrationOptions


class ColorInformation(ctypes.Structure):
    _fields_=[  ("infoCount",ctypes.c_int),
                ("saturation",ctypes.c_int),
                ("info",ctypes.POINTER(ctypes.c_double)) ]
PColorInformation=ctypes.POINTER(ColorInformation)
class CColorInformation(ctypes_wrap.CStructWrapper):
    _struct=ColorInformation


class LearnColorPatternOptions(ctypes.Structure):
    _fields_=[  ("learnMode",ctypes.c_int),
                ("featureMode",ctypes.c_int),
                ("threshold",ctypes.c_int),
                ("ignoreMode",ctypes.c_int),
                ("colorsToIgnore",ctypes.POINTER(ColorInformation)),
                ("numColorsToIgnore",ctypes.c_int) ]
PLearnColorPatternOptions=ctypes.POINTER(LearnColorPatternOptions)
class CLearnColorPatternOptions(ctypes_wrap.CStructWrapper):
    _struct=LearnColorPatternOptions


class Line(ctypes.Structure):
    _fields_=[  ("start",Point),
                ("end",Point) ]
PLine=ctypes.POINTER(Line)
class CLine(ctypes_wrap.CStructWrapper):
    _struct=Line


class LinearAverages(ctypes.Structure):
    _fields_=[  ("columnAverages",ctypes.POINTER(ctypes.c_float)),
                ("columnCount",ctypes.c_int),
                ("rowAverages",ctypes.POINTER(ctypes.c_float)),
                ("rowCount",ctypes.c_int),
                ("risingDiagAverages",ctypes.POINTER(ctypes.c_float)),
                ("risingDiagCount",ctypes.c_int),
                ("fallingDiagAverages",ctypes.POINTER(ctypes.c_float)),
                ("fallingDiagCount",ctypes.c_int) ]
PLinearAverages=ctypes.POINTER(LinearAverages)
class CLinearAverages(ctypes_wrap.CStructWrapper):
    _struct=LinearAverages


class LineProfile(ctypes.Structure):
    _fields_=[  ("profileData",ctypes.POINTER(ctypes.c_float)),
                ("boundingBox",Rect),
                ("min",ctypes.c_float),
                ("max",ctypes.c_float),
                ("mean",ctypes.c_float),
                ("stdDev",ctypes.c_float),
                ("dataCount",ctypes.c_int) ]
PLineProfile=ctypes.POINTER(LineProfile)
class CLineProfile(ctypes_wrap.CStructWrapper):
    _struct=LineProfile


class RotationAngleRange(ctypes.Structure):
    _fields_=[  ("lower",ctypes.c_float),
                ("upper",ctypes.c_float) ]
PRotationAngleRange=ctypes.POINTER(RotationAngleRange)
class CRotationAngleRange(ctypes_wrap.CStructWrapper):
    _struct=RotationAngleRange


class MatchColorPatternOptions(ctypes.Structure):
    _fields_=[  ("matchMode",ctypes.c_int),
                ("featureMode",ctypes.c_int),
                ("minContrast",ctypes.c_int),
                ("subpixelAccuracy",ctypes.c_int),
                ("angleRanges",ctypes.POINTER(RotationAngleRange)),
                ("numRanges",ctypes.c_int),
                ("colorWeight",ctypes.c_double),
                ("sensitivity",ctypes.c_int),
                ("strategy",ctypes.c_int),
                ("numMatchesRequested",ctypes.c_int),
                ("minMatchScore",ctypes.c_float) ]
PMatchColorPatternOptions=ctypes.POINTER(MatchColorPatternOptions)
class CMatchColorPatternOptions(ctypes_wrap.CStructWrapper):
    _struct=MatchColorPatternOptions


class HistogramReport(ctypes.Structure):
    _fields_=[  ("histogram",ctypes.POINTER(ctypes.c_int)),
                ("histogramCount",ctypes.c_int),
                ("min",ctypes.c_float),
                ("max",ctypes.c_float),
                ("start",ctypes.c_float),
                ("width",ctypes.c_float),
                ("mean",ctypes.c_float),
                ("stdDev",ctypes.c_float),
                ("numPixels",ctypes.c_int) ]
PHistogramReport=ctypes.POINTER(HistogramReport)
class CHistogramReport(ctypes_wrap.CStructWrapper):
    _struct=HistogramReport


class ArcInfo(ctypes.Structure):
    _fields_=[  ("boundingBox",Rect),
                ("startAngle",ctypes.c_double),
                ("endAngle",ctypes.c_double) ]
PArcInfo=ctypes.POINTER(ArcInfo)
class CArcInfo(ctypes_wrap.CStructWrapper):
    _struct=ArcInfo


class AxisReport(ctypes.Structure):
    _fields_=[  ("origin",PointFloat),
                ("mainAxisEnd",PointFloat),
                ("secondaryAxisEnd",PointFloat) ]
PAxisReport=ctypes.POINTER(AxisReport)
class CAxisReport(ctypes_wrap.CStructWrapper):
    _struct=AxisReport


class BarcodeGradingReport(ctypes.Structure):
    _fields_=[  ("overallGrade",ctypes.c_char),
                ("edgeDeterminationGrade",ctypes.c_char),
                ("minimumReflectanceGrade",ctypes.c_char),
                ("minimumContrastGrade",ctypes.c_char),
                ("symbolContrastGrade",ctypes.c_char),
                ("modulationGrade",ctypes.c_char),
                ("defectsGrade",ctypes.c_char),
                ("decodeGrade",ctypes.c_char),
                ("decodabilityGrade",ctypes.c_char),
                ("quietZone",ctypes.c_char) ]
PBarcodeGradingReport=ctypes.POINTER(BarcodeGradingReport)
class CBarcodeGradingReport(ctypes_wrap.CStructWrapper):
    _struct=BarcodeGradingReport


class BarcodeGradingOptions(ctypes.Structure):
    _fields_=[  ("calcGradingReport",ctypes.c_int),
                ("scanProfileWidth",ctypes.c_uint) ]
PBarcodeGradingOptions=ctypes.POINTER(BarcodeGradingOptions)
class CBarcodeGradingOptions(ctypes_wrap.CStructWrapper):
    _struct=BarcodeGradingOptions


class BarcodeInfo(ctypes.Structure):
    _fields_=[  ("outputString",ctypes.c_char_p),
                ("size",ctypes.c_int),
                ("outputChar1",ctypes.c_char),
                ("outputChar2",ctypes.c_char),
                ("confidenceLevel",ctypes.c_double),
                ("type",ctypes.c_int) ]
PBarcodeInfo=ctypes.POINTER(BarcodeInfo)
class CBarcodeInfo(ctypes_wrap.CStructWrapper):
    _struct=BarcodeInfo


class BarcodeInfoReport(ctypes.Structure):
    _fields_=[  ("info",ctypes.POINTER(BarcodeInfo2)),
                ("numBarcodes",ctypes.c_uint) ]
PBarcodeInfoReport=ctypes.POINTER(BarcodeInfoReport)
class CBarcodeInfoReport(ctypes_wrap.CStructWrapper):
    _struct=BarcodeInfoReport


class BarcodeInfoReportandGrading(ctypes.Structure):
    _fields_=[  ("info",ctypes.POINTER(BarcodeInfo2)),
                ("numBarcodes",ctypes.c_uint),
                ("gradingReport",ctypes.POINTER(BarcodeGradingReport)) ]
PBarcodeInfoReportandGrading=ctypes.POINTER(BarcodeInfoReportandGrading)
class CBarcodeInfoReportandGrading(ctypes_wrap.CStructWrapper):
    _struct=BarcodeInfoReportandGrading


class BCGOptions(ctypes.Structure):
    _fields_=[  ("brightness",ctypes.c_float),
                ("contrast",ctypes.c_float),
                ("gamma",ctypes.c_float) ]
PBCGOptions=ctypes.POINTER(BCGOptions)
class CBCGOptions(ctypes_wrap.CStructWrapper):
    _struct=BCGOptions


class BestCircle(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("radius",ctypes.c_double),
                ("area",ctypes.c_double),
                ("perimeter",ctypes.c_double),
                ("error",ctypes.c_double) ]
PBestCircle=ctypes.POINTER(BestCircle)
class CBestCircle(ctypes_wrap.CStructWrapper):
    _struct=BestCircle


class BestEllipse(ctypes.Structure):
    _fields_=[  ("center",PointFloat),
                ("majorAxisStart",PointFloat),
                ("majorAxisEnd",PointFloat),
                ("minorAxisStart",PointFloat),
                ("minorAxisEnd",PointFloat),
                ("area",ctypes.c_double),
                ("perimeter",ctypes.c_double) ]
PBestEllipse=ctypes.POINTER(BestEllipse)
class CBestEllipse(ctypes_wrap.CStructWrapper):
    _struct=BestEllipse


class BestLine(ctypes.Structure):
    _fields_=[  ("start",PointFloat),
                ("end",PointFloat),
                ("equation",LineEquation),
                ("valid",ctypes.c_int),
                ("error",ctypes.c_double),
                ("pointsUsed",ctypes.POINTER(ctypes.c_int)),
                ("numPointsUsed",ctypes.c_int) ]
PBestLine=ctypes.POINTER(BestLine)
class CBestLine(ctypes_wrap.CStructWrapper):
    _struct=BestLine


class BrowserOptions(ctypes.Structure):
    _fields_=[  ("width",ctypes.c_int),
                ("height",ctypes.c_int),
                ("imagesPerLine",ctypes.c_int),
                ("backgroundColor",RGBValue),
                ("frameSize",ctypes.c_int),
                ("style",ctypes.c_int),
                ("ratio",ctypes.c_float),
                ("focusColor",RGBValue) ]
PBrowserOptions=ctypes.POINTER(BrowserOptions)
class CBrowserOptions(ctypes_wrap.CStructWrapper):
    _struct=BrowserOptions


class CoordinateSystem(ctypes.Structure):
    _fields_=[  ("origin",PointFloat),
                ("angle",ctypes.c_float),
                ("axisOrientation",ctypes.c_int) ]
PCoordinateSystem=ctypes.POINTER(CoordinateSystem)
class CCoordinateSystem(ctypes_wrap.CStructWrapper):
    _struct=CoordinateSystem


class CalibrationInfo(ctypes.Structure):
    _fields_=[  ("errorMap",ctypes.POINTER(ctypes.c_float)),
                ("mapColumns",ctypes.c_int),
                ("mapRows",ctypes.c_int),
                ("userRoi",ctypes.c_void_p),
                ("calibrationRoi",ctypes.c_void_p),
                ("options",LearnCalibrationOptions),
                ("grid",GridDescriptor),
                ("system",CoordinateSystem),
                ("range",RangeFloat),
                ("quality",ctypes.c_float) ]
PCalibrationInfo=ctypes.POINTER(CalibrationInfo)
class CCalibrationInfo(ctypes_wrap.CStructWrapper):
    _struct=CalibrationInfo


class CalibrationPoints(ctypes.Structure):
    _fields_=[  ("pixelCoordinates",ctypes.POINTER(PointFloat)),
                ("realWorldCoordinates",ctypes.POINTER(PointFloat)),
                ("numCoordinates",ctypes.c_int) ]
PCalibrationPoints=ctypes.POINTER(CalibrationPoints)
class CCalibrationPoints(ctypes_wrap.CStructWrapper):
    _struct=CalibrationPoints


class CaliperOptions(ctypes.Structure):
    _fields_=[  ("polarity",ctypes.c_int),
                ("separation",ctypes.c_float),
                ("separationDeviation",ctypes.c_float) ]
PCaliperOptions=ctypes.POINTER(CaliperOptions)
class CCaliperOptions(ctypes_wrap.CStructWrapper):
    _struct=CaliperOptions


class CaliperReport(ctypes.Structure):
    _fields_=[  ("edge1Contrast",ctypes.c_float),
                ("edge1Coord",PointFloat),
                ("edge2Contrast",ctypes.c_float),
                ("edge2Coord",PointFloat),
                ("separation",ctypes.c_float),
                ("reserved",ctypes.c_float) ]
PCaliperReport=ctypes.POINTER(CaliperReport)
class CCaliperReport(ctypes_wrap.CStructWrapper):
    _struct=CaliperReport


class DrawTextOptions(ctypes.Structure):
    _fields_=[  ("fontName",ctypes.c_char*32),
                ("fontSize",ctypes.c_int),
                ("bold",ctypes.c_int),
                ("italic",ctypes.c_int),
                ("underline",ctypes.c_int),
                ("strikeout",ctypes.c_int),
                ("textAlignment",ctypes.c_int),
                ("fontColor",ctypes.c_int) ]
PDrawTextOptions=ctypes.POINTER(DrawTextOptions)
class CDrawTextOptions(ctypes_wrap.CStructWrapper):
    _struct=DrawTextOptions


class CircleReport(ctypes.Structure):
    _fields_=[  ("center",Point),
                ("radius",ctypes.c_int),
                ("area",ctypes.c_int) ]
PCircleReport=ctypes.POINTER(CircleReport)
class CCircleReport(ctypes_wrap.CStructWrapper):
    _struct=CircleReport


class ClosedContour(ctypes.Structure):
    _fields_=[  ("points",ctypes.POINTER(Point)),
                ("numPoints",ctypes.c_int) ]
PClosedContour=ctypes.POINTER(ClosedContour)
class CClosedContour(ctypes_wrap.CStructWrapper):
    _struct=ClosedContour


class ColorHistogramReport(ctypes.Structure):
    _fields_=[  ("plane1",HistogramReport),
                ("plane2",HistogramReport),
                ("plane3",HistogramReport) ]
PColorHistogramReport=ctypes.POINTER(ColorHistogramReport)
class CColorHistogramReport(ctypes_wrap.CStructWrapper):
    _struct=ColorHistogramReport


class Complex(ctypes.Structure):
    _fields_=[  ("r",ctypes.c_float),
                ("i",ctypes.c_float) ]
PComplex=ctypes.POINTER(Complex)
class CComplex(ctypes_wrap.CStructWrapper):
    _struct=Complex


class ConcentricRakeReport(ctypes.Structure):
    _fields_=[  ("rakeArcs",ctypes.POINTER(ArcInfo)),
                ("numArcs",ctypes.c_int),
                ("firstEdges",ctypes.POINTER(PointFloat)),
                ("numFirstEdges",ctypes.c_int),
                ("lastEdges",ctypes.POINTER(PointFloat)),
                ("numLastEdges",ctypes.c_int),
                ("allEdges",ctypes.POINTER(EdgeLocationReport)),
                ("linesWithEdges",ctypes.POINTER(ctypes.c_int)),
                ("numLinesWithEdges",ctypes.c_int) ]
PConcentricRakeReport=ctypes.POINTER(ConcentricRakeReport)
class CConcentricRakeReport(ctypes_wrap.CStructWrapper):
    _struct=ConcentricRakeReport


class ConstructROIOptions(ctypes.Structure):
    _fields_=[  ("windowNumber",ctypes.c_int),
                ("windowTitle",ctypes.c_char_p),
                ("type",ctypes.c_int),
                ("palette",ctypes.POINTER(RGBValue)),
                ("numColors",ctypes.c_int) ]
PConstructROIOptions=ctypes.POINTER(ConstructROIOptions)
class CConstructROIOptions(ctypes_wrap.CStructWrapper):
    _struct=ConstructROIOptions


class ContourInfo(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("numPoints",ctypes.c_uint),
                ("points",ctypes.POINTER(Point)),
                ("contourColor",RGBValue) ]
PContourInfo=ctypes.POINTER(ContourInfo)
class CContourInfo(ctypes_wrap.CStructWrapper):
    _struct=ContourInfo


class OpenContour(ctypes.Structure):
    _fields_=[  ("points",ctypes.POINTER(Point)),
                ("numPoints",ctypes.c_int) ]
POpenContour=ctypes.POINTER(OpenContour)
class COpenContour(ctypes_wrap.CStructWrapper):
    _struct=OpenContour


class RotatedRect(ctypes.Structure):
    _fields_=[  ("top",ctypes.c_int),
                ("left",ctypes.c_int),
                ("height",ctypes.c_int),
                ("width",ctypes.c_int),
                ("angle",ctypes.c_double) ]
PRotatedRect=ctypes.POINTER(RotatedRect)
class CRotatedRect(ctypes_wrap.CStructWrapper):
    _struct=RotatedRect


class ContourInfo2(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("color",RGBValue),
                ("structure",ctypes.c_void_p) ]
PContourInfo2=ctypes.POINTER(ContourInfo2)
class CContourInfo2(ctypes_wrap.CStructWrapper):
    _struct=ContourInfo2


class ContourPoint(ctypes.Structure):
    _fields_=[  ("x",ctypes.c_double),
                ("y",ctypes.c_double),
                ("curvature",ctypes.c_double),
                ("xDisplacement",ctypes.c_double),
                ("yDisplacement",ctypes.c_double) ]
PContourPoint=ctypes.POINTER(ContourPoint)
class CContourPoint(ctypes_wrap.CStructWrapper):
    _struct=ContourPoint


class CoordinateTransform(ctypes.Structure):
    _fields_=[  ("initialOrigin",Point),
                ("initialAngle",ctypes.c_float),
                ("finalOrigin",Point),
                ("finalAngle",ctypes.c_float) ]
PCoordinateTransform=ctypes.POINTER(CoordinateTransform)
class CCoordinateTransform(ctypes_wrap.CStructWrapper):
    _struct=CoordinateTransform


class CoordinateTransform2(ctypes.Structure):
    _fields_=[  ("referenceSystem",CoordinateSystem),
                ("measurementSystem",CoordinateSystem) ]
PCoordinateTransform2=ctypes.POINTER(CoordinateTransform2)
class CCoordinateTransform2(ctypes_wrap.CStructWrapper):
    _struct=CoordinateTransform2


class CannyOptions(ctypes.Structure):
    _fields_=[  ("sigma",ctypes.c_float),
                ("upperThreshold",ctypes.c_float),
                ("lowerThreshold",ctypes.c_float),
                ("windowSize",ctypes.c_int) ]
PCannyOptions=ctypes.POINTER(CannyOptions)
class CCannyOptions(ctypes_wrap.CStructWrapper):
    _struct=CannyOptions


class DetectorReport(ctypes.Structure):
    _fields_=[  ("featureCoordinates",ctypes.POINTER(PointFloat)),
                ("numfeatures",ctypes.c_uint),
                ("featureScores",ctypes.POINTER(ctypes.c_double)),
                ("featureCoordinatesReal",ctypes.POINTER(PointFloat)),
                ("calibrationValid",ctypes.POINTER(ctypes.c_uint)) ]
PDetectorReport=ctypes.POINTER(DetectorReport)
class CDetectorReport(ctypes_wrap.CStructWrapper):
    _struct=DetectorReport


class FeatureDescriptor(ctypes.Structure):
    _fields_=[  ("desc",ctypes.POINTER(ctypes.c_ubyte)),
                ("size",ctypes.c_uint) ]
PFeatureDescriptor=ctypes.POINTER(FeatureDescriptor)
class CFeatureDescriptor(ctypes_wrap.CStructWrapper):
    _struct=FeatureDescriptor


class DescriptorReport(ctypes.Structure):
    _fields_=[  ("featureCoordinates",ctypes.POINTER(PointFloat)),
                ("numfeatures",ctypes.c_uint),
                ("descriptor",ctypes.POINTER(FeatureDescriptor)) ]
PDescriptorReport=ctypes.POINTER(DescriptorReport)
class CDescriptorReport(ctypes_wrap.CStructWrapper):
    _struct=DescriptorReport


class ExtractorReport(ctypes.Structure):
    _fields_=[  ("features",ctypes.POINTER(ctypes.c_float)),
                ("numfeatures",ctypes.c_uint) ]
PExtractorReport=ctypes.POINTER(ExtractorReport)
class CExtractorReport(ctypes_wrap.CStructWrapper):
    _struct=ExtractorReport


class MatchedPoint(ctypes.Structure):
    _fields_=[  ("first",PointFloat),
                ("second",PointFloat) ]
PMatchedPoint=ctypes.POINTER(MatchedPoint)
class CMatchedPoint(ctypes_wrap.CStructWrapper):
    _struct=MatchedPoint


class FeatureMatchingReport(ctypes.Structure):
    _fields_=[  ("matches",ctypes.POINTER(MatchedPoint)),
                ("numMatches",ctypes.c_uint),
                ("matchScores",ctypes.POINTER(ctypes.c_double)),
                ("homographyMatrix",ctypes.POINTER(ctypes.c_double)) ]
PFeatureMatchingReport=ctypes.POINTER(FeatureMatchingReport)
class CFeatureMatchingReport(ctypes_wrap.CStructWrapper):
    _struct=FeatureMatchingReport


class UserPointSymbol(ctypes.Structure):
    _fields_=[  ("cols",ctypes.c_int),
                ("rows",ctypes.c_int),
                ("pixels",ctypes.POINTER(ctypes.c_int)) ]
PUserPointSymbol=ctypes.POINTER(UserPointSymbol)
class CUserPointSymbol(ctypes_wrap.CStructWrapper):
    _struct=UserPointSymbol


class View3DOptions(ctypes.Structure):
    _fields_=[  ("sizeReduction",ctypes.c_int),
                ("maxHeight",ctypes.c_int),
                ("direction",ctypes.c_int),
                ("alpha",ctypes.c_float),
                ("beta",ctypes.c_float),
                ("border",ctypes.c_int),
                ("background",ctypes.c_int),
                ("plane",ctypes.c_int) ]
PView3DOptions=ctypes.POINTER(View3DOptions)
class CView3DOptions(ctypes_wrap.CStructWrapper):
    _struct=View3DOptions


class MatchPatternOptions(ctypes.Structure):
    _fields_=[  ("mode",ctypes.c_int),
                ("minContrast",ctypes.c_int),
                ("subpixelAccuracy",ctypes.c_int),
                ("angleRanges",ctypes.POINTER(RotationAngleRange)),
                ("numRanges",ctypes.c_int),
                ("numMatchesRequested",ctypes.c_int),
                ("matchFactor",ctypes.c_int),
                ("minMatchScore",ctypes.c_float) ]
PMatchPatternOptions=ctypes.POINTER(MatchPatternOptions)
class CMatchPatternOptions(ctypes_wrap.CStructWrapper):
    _struct=MatchPatternOptions


class MatchPatternOptions2(ctypes.Structure):
    _fields_=[  ("algorithm",ctypes.c_int),
                ("angleRanges",ctypes.POINTER(RotationAngleRange)),
                ("numRanges",ctypes.c_int),
                ("numMatchesRequested",ctypes.c_int),
                ("matchFactor",ctypes.c_int),
                ("minMatchScore",ctypes.c_float) ]
PMatchPatternOptions2=ctypes.POINTER(MatchPatternOptions2)
class CMatchPatternOptions2(ctypes_wrap.CStructWrapper):
    _struct=MatchPatternOptions2


class TIFFFileOptions(ctypes.Structure):
    _fields_=[  ("rowsPerStrip",ctypes.c_int),
                ("photoInterp",ctypes.c_int),
                ("compressionType",ctypes.c_int) ]
PTIFFFileOptions=ctypes.POINTER(TIFFFileOptions)
class CTIFFFileOptions(ctypes_wrap.CStructWrapper):
    _struct=TIFFFileOptions


class OverlayTextOptions(ctypes.Structure):
    _fields_=[  ("fontName",ctypes.c_char_p),
                ("fontSize",ctypes.c_int),
                ("bold",ctypes.c_int),
                ("italic",ctypes.c_int),
                ("underline",ctypes.c_int),
                ("strikeout",ctypes.c_int),
                ("horizontalTextAlignment",ctypes.c_int),
                ("verticalTextAlignment",ctypes.c_int),
                ("backgroundColor",RGBValue),
                ("angle",ctypes.c_double) ]
POverlayTextOptions=ctypes.POINTER(OverlayTextOptions)
class COverlayTextOptions(ctypes_wrap.CStructWrapper):
    _struct=OverlayTextOptions


class ParticleFilterCriteria(ctypes.Structure):
    _fields_=[  ("parameter",ctypes.c_int),
                ("lower",ctypes.c_float),
                ("upper",ctypes.c_float),
                ("exclude",ctypes.c_int) ]
PParticleFilterCriteria=ctypes.POINTER(ParticleFilterCriteria)
class CParticleFilterCriteria(ctypes_wrap.CStructWrapper):
    _struct=ParticleFilterCriteria


class ParticleReport(ctypes.Structure):
    _fields_=[  ("area",ctypes.c_int),
                ("calibratedArea",ctypes.c_float),
                ("perimeter",ctypes.c_float),
                ("numHoles",ctypes.c_int),
                ("areaOfHoles",ctypes.c_int),
                ("perimeterOfHoles",ctypes.c_float),
                ("boundingBox",Rect),
                ("sigmaX",ctypes.c_float),
                ("sigmaY",ctypes.c_float),
                ("sigmaXX",ctypes.c_float),
                ("sigmaYY",ctypes.c_float),
                ("sigmaXY",ctypes.c_float),
                ("longestLength",ctypes.c_int),
                ("longestPoint",Point),
                ("projectionX",ctypes.c_int),
                ("projectionY",ctypes.c_int),
                ("connect8",ctypes.c_int) ]
PParticleReport=ctypes.POINTER(ParticleReport)
class CParticleReport(ctypes_wrap.CStructWrapper):
    _struct=ParticleReport


class PatternMatch(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("rotation",ctypes.c_float),
                ("scale",ctypes.c_float),
                ("score",ctypes.c_float),
                ("corner",PointFloat*4) ]
PPatternMatch=ctypes.POINTER(PatternMatch)
class CPatternMatch(ctypes_wrap.CStructWrapper):
    _struct=PatternMatch


class PatternMatchReport(ctypes.Structure):
    _fields_=[  ("position",PointFloat),
                ("calibratedPosition",PointFloat),
                ("rotation",ctypes.c_float),
                ("calibratedRotation",ctypes.c_float),
                ("scale",ctypes.c_float),
                ("calibratedScale",ctypes.c_float),
                ("score",ctypes.c_float),
                ("calibratedScore",ctypes.c_float),
                ("corner",PointFloat*4),
                ("calibratedCorner",PointFloat*4) ]
PPatternMatchReport=ctypes.POINTER(PatternMatchReport)
class CPatternMatchReport(ctypes_wrap.CStructWrapper):
    _struct=PatternMatchReport


class PMLearnAdvancedSetupDataOption(ctypes.Structure):
    _fields_=[  ("learnSetupOption",ctypes.c_int),
                ("value",ctypes.c_double) ]
PPMLearnAdvancedSetupDataOption=ctypes.POINTER(PMLearnAdvancedSetupDataOption)
class CPMLearnAdvancedSetupDataOption(ctypes_wrap.CStructWrapper):
    _struct=PMLearnAdvancedSetupDataOption


class PMMatchAdvancedSetupDataOption(ctypes.Structure):
    _fields_=[  ("matchSetupOption",ctypes.c_int),
                ("value",ctypes.c_double) ]
PPMMatchAdvancedSetupDataOption=ctypes.POINTER(PMMatchAdvancedSetupDataOption)
class CPMMatchAdvancedSetupDataOption(ctypes_wrap.CStructWrapper):
    _struct=PMMatchAdvancedSetupDataOption


class PresetOption(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("value",ctypes.c_double) ]
PPresetOption=ctypes.POINTER(PresetOption)
class CPresetOption(ctypes_wrap.CStructWrapper):
    _struct=PresetOption


class QuantifyData(ctypes.Structure):
    _fields_=[  ("mean",ctypes.c_float),
                ("stdDev",ctypes.c_float),
                ("min",ctypes.c_float),
                ("max",ctypes.c_float),
                ("calibratedArea",ctypes.c_float),
                ("pixelArea",ctypes.c_int),
                ("relativeSize",ctypes.c_float) ]
PQuantifyData=ctypes.POINTER(QuantifyData)
class CQuantifyData(ctypes_wrap.CStructWrapper):
    _struct=QuantifyData


class QuantifyData2(ctypes.Structure):
    _fields_=[  ("mean",ctypes.c_float),
                ("stdDev",ctypes.c_float),
                ("min",ctypes.c_float),
                ("max",ctypes.c_float),
                ("calibratedArea",ctypes.c_float),
                ("pixelArea",ctypes.c_int),
                ("relativeSize",ctypes.c_float),
                ("calibrationValid",ctypes.c_uint) ]
PQuantifyData2=ctypes.POINTER(QuantifyData2)
class CQuantifyData2(ctypes_wrap.CStructWrapper):
    _struct=QuantifyData2


class QuantifyReport(ctypes.Structure):
    _fields_=[  ("global",QuantifyData),
                ("regions",ctypes.POINTER(QuantifyData)),
                ("regionCount",ctypes.c_int) ]
PQuantifyReport=ctypes.POINTER(QuantifyReport)
class CQuantifyReport(ctypes_wrap.CStructWrapper):
    _struct=QuantifyReport


class QuantifyReport2(ctypes.Structure):
    _fields_=[  ("global",QuantifyData2),
                ("regions",ctypes.POINTER(QuantifyData2)),
                ("regionCount",ctypes.c_uint) ]
PQuantifyReport2=ctypes.POINTER(QuantifyReport2)
class CQuantifyReport2(ctypes_wrap.CStructWrapper):
    _struct=QuantifyReport2


class RakeOptions(ctypes.Structure):
    _fields_=[  ("threshold",ctypes.c_int),
                ("width",ctypes.c_int),
                ("steepness",ctypes.c_int),
                ("subsamplingRatio",ctypes.c_int),
                ("subpixelType",ctypes.c_int),
                ("subpixelDivisions",ctypes.c_int) ]
PRakeOptions=ctypes.POINTER(RakeOptions)
class CRakeOptions(ctypes_wrap.CStructWrapper):
    _struct=RakeOptions


class RakeReport(ctypes.Structure):
    _fields_=[  ("rakeLines",ctypes.POINTER(LineFloat)),
                ("numRakeLines",ctypes.c_int),
                ("firstEdges",ctypes.POINTER(PointFloat)),
                ("numFirstEdges",ctypes.c_uint),
                ("lastEdges",ctypes.POINTER(PointFloat)),
                ("numLastEdges",ctypes.c_uint),
                ("allEdges",ctypes.POINTER(EdgeLocationReport)),
                ("linesWithEdges",ctypes.POINTER(ctypes.c_int)),
                ("numLinesWithEdges",ctypes.c_int) ]
PRakeReport=ctypes.POINTER(RakeReport)
class CRakeReport(ctypes_wrap.CStructWrapper):
    _struct=RakeReport


class TransformReport(ctypes.Structure):
    _fields_=[  ("points",ctypes.POINTER(PointFloat)),
                ("validPoints",ctypes.POINTER(ctypes.c_int)),
                ("numPoints",ctypes.c_int) ]
PTransformReport=ctypes.POINTER(TransformReport)
class CTransformReport(ctypes_wrap.CStructWrapper):
    _struct=TransformReport


class ShapeReport(ctypes.Structure):
    _fields_=[  ("coordinates",Rect),
                ("centroid",Point),
                ("size",ctypes.c_int),
                ("score",ctypes.c_double) ]
PShapeReport=ctypes.POINTER(ShapeReport)
class CShapeReport(ctypes_wrap.CStructWrapper):
    _struct=ShapeReport


class ShapeReport2(ctypes.Structure):
    _fields_=[  ("coordinates",Rect),
                ("centroid",PointFloat),
                ("size",ctypes.c_int),
                ("score",ctypes.c_double) ]
PShapeReport2=ctypes.POINTER(ShapeReport2)
class CShapeReport2(ctypes_wrap.CStructWrapper):
    _struct=ShapeReport2


class MeterArc(ctypes.Structure):
    _fields_=[  ("needleBase",PointFloat),
                ("arcCoordPoints",ctypes.POINTER(PointFloat)),
                ("numOfArcCoordPoints",ctypes.c_int),
                ("needleColor",ctypes.c_int) ]
PMeterArc=ctypes.POINTER(MeterArc)
class CMeterArc(ctypes_wrap.CStructWrapper):
    _struct=MeterArc


class ThresholdData(ctypes.Structure):
    _fields_=[  ("rangeMin",ctypes.c_float),
                ("rangeMax",ctypes.c_float),
                ("newValue",ctypes.c_float),
                ("useNewValue",ctypes.c_int) ]
PThresholdData=ctypes.POINTER(ThresholdData)
class CThresholdData(ctypes_wrap.CStructWrapper):
    _struct=ThresholdData


class StructuringElement(ctypes.Structure):
    _fields_=[  ("matrixCols",ctypes.c_int),
                ("matrixRows",ctypes.c_int),
                ("hexa",ctypes.c_int),
                ("kernel",ctypes.POINTER(ctypes.c_int)) ]
PStructuringElement=ctypes.POINTER(StructuringElement)
class CStructuringElement(ctypes_wrap.CStructWrapper):
    _struct=StructuringElement


class SpokeReport(ctypes.Structure):
    _fields_=[  ("spokeLines",ctypes.POINTER(LineFloat)),
                ("numSpokeLines",ctypes.c_int),
                ("firstEdges",ctypes.POINTER(PointFloat)),
                ("numFirstEdges",ctypes.c_int),
                ("lastEdges",ctypes.POINTER(PointFloat)),
                ("numLastEdges",ctypes.c_int),
                ("allEdges",ctypes.POINTER(EdgeLocationReport)),
                ("linesWithEdges",ctypes.POINTER(ctypes.c_int)),
                ("numLinesWithEdges",ctypes.c_int) ]
PSpokeReport=ctypes.POINTER(SpokeReport)
class CSpokeReport(ctypes_wrap.CStructWrapper):
    _struct=SpokeReport


class SimpleEdgeOptions(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("threshold",ctypes.c_int),
                ("hysteresis",ctypes.c_int),
                ("process",ctypes.c_int),
                ("subpixel",ctypes.c_int) ]
PSimpleEdgeOptions=ctypes.POINTER(SimpleEdgeOptions)
class CSimpleEdgeOptions(ctypes_wrap.CStructWrapper):
    _struct=SimpleEdgeOptions


class SelectParticleCriteria(ctypes.Structure):
    _fields_=[  ("parameter",ctypes.c_int),
                ("lower",ctypes.c_float),
                ("upper",ctypes.c_float) ]
PSelectParticleCriteria=ctypes.POINTER(SelectParticleCriteria)
class CSelectParticleCriteria(ctypes_wrap.CStructWrapper):
    _struct=SelectParticleCriteria


class SegmentInfo(ctypes.Structure):
    _fields_=[  ("numberOfPoints",ctypes.c_int),
                ("isOpen",ctypes.c_int),
                ("weight",ctypes.c_double),
                ("points",ctypes.POINTER(ContourPoint)) ]
PSegmentInfo=ctypes.POINTER(SegmentInfo)
class CSegmentInfo(ctypes_wrap.CStructWrapper):
    _struct=SegmentInfo


class PyramidInfoStruct(ctypes.Structure):
    _fields_=[  ("maxPyramidLevel",ctypes.c_int),
                ("optimalPyramidLevel",ctypes.c_int),
                ("maxPyramidLevelToStoreData",ctypes.c_int) ]
PPyramidInfoStruct=ctypes.POINTER(PyramidInfoStruct)
class CPyramidInfoStruct(ctypes_wrap.CStructWrapper):
    _struct=PyramidInfoStruct


class MatchOffsetInfoStruct(ctypes.Structure):
    _fields_=[  ("matchOffsetX",ctypes.c_double),
                ("matchOffsetY",ctypes.c_double),
                ("angleOffset",ctypes.c_double) ]
PMatchOffsetInfoStruct=ctypes.POINTER(MatchOffsetInfoStruct)
class CMatchOffsetInfoStruct(ctypes_wrap.CStructWrapper):
    _struct=MatchOffsetInfoStruct


class PatternMatchTemplateInformation(ctypes.Structure):
    _fields_=[  ("advancedOptionsPointer",ctypes.POINTER(PMMatchAdvancedSetupDataOption)),
                ("numAdvancedOptions",ctypes.c_int),
                ("presetOptionsPointer",ctypes.POINTER(PresetOption)),
                ("numPresetOptions",ctypes.c_int),
                ("pyramidInfo",PyramidInfoStruct),
                ("matchOffsetInfo",MatchOffsetInfoStruct) ]
PPatternMatchTemplateInformation=ctypes.POINTER(PatternMatchTemplateInformation)
class CPatternMatchTemplateInformation(ctypes_wrap.CStructWrapper):
    _struct=PatternMatchTemplateInformation


class GeometricMatchTemplateInformation(ctypes.Structure):
    _fields_=[  ("GPMadvancedOptionsPointer",ctypes.POINTER(GeometricAdvancedSetupDataOption)),
                ("numAdvancedOptions",ctypes.c_int),
                ("presetOptionsPointer",ctypes.POINTER(PresetOption)),
                ("numPresetOptions",ctypes.c_int),
                ("_curveParameters",CurveParameters),
                ("matchOffsetInfo",MatchOffsetInfoStruct) ]
PGeometricMatchTemplateInformation=ctypes.POINTER(GeometricMatchTemplateInformation)
class CGeometricMatchTemplateInformation(ctypes_wrap.CStructWrapper):
    _struct=GeometricMatchTemplateInformation


class ROIProfile(ctypes.Structure):
    _fields_=[  ("report",LineProfile),
                ("pixels",ctypes.POINTER(Point)) ]
PROIProfile=ctypes.POINTER(ROIProfile)
class CROIProfile(ctypes_wrap.CStructWrapper):
    _struct=ROIProfile


class ToolWindowOptions(ctypes.Structure):
    _fields_=[  ("showSelectionTool",ctypes.c_int),
                ("showZoomTool",ctypes.c_int),
                ("showPointTool",ctypes.c_int),
                ("showLineTool",ctypes.c_int),
                ("showRectangleTool",ctypes.c_int),
                ("showOvalTool",ctypes.c_int),
                ("showPolygonTool",ctypes.c_int),
                ("showClosedFreehandTool",ctypes.c_int),
                ("showPolyLineTool",ctypes.c_int),
                ("showFreehandTool",ctypes.c_int),
                ("showAnnulusTool",ctypes.c_int),
                ("showRotatedRectangleTool",ctypes.c_int),
                ("showPanTool",ctypes.c_int),
                ("showZoomOutTool",ctypes.c_int),
                ("reserved2",ctypes.c_int),
                ("reserved3",ctypes.c_int),
                ("reserved4",ctypes.c_int) ]
PToolWindowOptions=ctypes.POINTER(ToolWindowOptions)
class CToolWindowOptions(ctypes_wrap.CStructWrapper):
    _struct=ToolWindowOptions


class SpokeOptions(ctypes.Structure):
    _fields_=[  ("threshold",ctypes.c_int),
                ("width",ctypes.c_int),
                ("steepness",ctypes.c_int),
                ("subsamplingRatio",ctypes.c_double),
                ("subpixelType",ctypes.c_int),
                ("subpixelDivisions",ctypes.c_int) ]
PSpokeOptions=ctypes.POINTER(SpokeOptions)
class CSpokeOptions(ctypes_wrap.CStructWrapper):
    _struct=SpokeOptions


class TemplateReport(ctypes.Structure):
    _fields_=[  ("templateContrast",ctypes.c_int),
                ("grayvalueMaxPyramidLevel",ctypes.c_int),
                ("grayvalueOptimalPyramidLevel",ctypes.c_int),
                ("gradientMaxPyramidLevel",ctypes.c_int),
                ("gradientOptimalPyramidLevel",ctypes.c_int) ]
PTemplateReport=ctypes.POINTER(TemplateReport)
class CTemplateReport(ctypes_wrap.CStructWrapper):
    _struct=TemplateReport


class ExtractTetragonOptions(ctypes.Structure):
    _fields_=[  ("interpolationMethod",ctypes.c_int),
                ("destinationWidth",ctypes.c_uint),
                ("destinationHeight",ctypes.c_uint),
                ("fillValue",ctypes.c_float) ]
PExtractTetragonOptions=ctypes.POINTER(ExtractTetragonOptions)
class CExtractTetragonOptions(ctypes_wrap.CStructWrapper):
    _struct=ExtractTetragonOptions


class SSIMComponents(ctypes.Structure):
    _fields_=[  ("luminance",ctypes.c_double),
                ("contrastAndStructural",ctypes.c_double) ]
PSSIMComponents=ctypes.POINTER(SSIMComponents)
class CSSIMComponents(ctypes_wrap.CStructWrapper):
    _struct=SSIMComponents


class BlockSize(ctypes.Structure):
    _fields_=[  ("xRes",ctypes.c_int),
                ("yRes",ctypes.c_int) ]
PBlockSize=ctypes.POINTER(BlockSize)
class CBlockSize(ctypes_wrap.CStructWrapper):
    _struct=BlockSize


class RectSize(ctypes.Structure):
    _fields_=[  ("windowWidth",ctypes.c_int),
                ("windowHeight",ctypes.c_int) ]
PRectSize=ctypes.POINTER(RectSize)
class CRectSize(ctypes_wrap.CStructWrapper):
    _struct=RectSize


class BlockStatistics(ctypes.Structure):
    _fields_=[  ("mean",ctypes.c_double),
                ("stdDeviation",ctypes.c_double),
                ("minValue",ctypes.c_double),
                ("maxValue",ctypes.c_double) ]
PBlockStatistics=ctypes.POINTER(BlockStatistics)
class CBlockStatistics(ctypes_wrap.CStructWrapper):
    _struct=BlockStatistics


class LKPyramidOptions(ctypes.Structure):
    _fields_=[  ("level",ctypes.c_int),
                ("maxIteration",ctypes.c_int),
                ("windowSize",ctypes.c_int),
                ("threshold",ctypes.c_double) ]
PLKPyramidOptions=ctypes.POINTER(LKPyramidOptions)
class CLKPyramidOptions(ctypes_wrap.CStructWrapper):
    _struct=LKPyramidOptions


class BlockStatisticsReport(ctypes.Structure):
    _fields_=[  ("blockStatistics",ctypes.POINTER(BlockStatistics)),
                ("totalNumOfBlocks",ctypes.c_uint),
                ("numofBlocksinXdir",ctypes.c_int),
                ("numofBlocksinYdir",ctypes.c_int) ]
PBlockStatisticsReport=ctypes.POINTER(BlockStatisticsReport)
class CBlockStatisticsReport(ctypes_wrap.CStructWrapper):
    _struct=BlockStatisticsReport


class FeaturePoints(ctypes.Structure):
    _fields_=[  ("points",ctypes.POINTER(PointFloat)),
                ("numPoints",ctypes.c_uint) ]
PFeaturePoints=ctypes.POINTER(FeaturePoints)
class CFeaturePoints(ctypes_wrap.CStructWrapper):
    _struct=FeaturePoints


class RectDouble(ctypes.Structure):
    _fields_=[  ("Left",ctypes.c_double),
                ("Top",ctypes.c_double),
                ("Right",ctypes.c_double),
                ("Bottom",ctypes.c_double) ]
PRectDouble=ctypes.POINTER(RectDouble)
class CRectDouble(ctypes_wrap.CStructWrapper):
    _struct=RectDouble


class DifferenceArray(ctypes.Structure):
    _fields_=[  ("difference",ctypes.POINTER(ctypes.c_double)),
                ("arraySize",ctypes.c_uint) ]
PDifferenceArray=ctypes.POINTER(DifferenceArray)
class CDifferenceArray(ctypes_wrap.CStructWrapper):
    _struct=DifferenceArray


class StoppingCriteria(ctypes.Structure):
    _fields_=[  ("type",ctypes.c_int),
                ("maxIterations",ctypes.c_int),
                ("epsilon",ctypes.c_double) ]
PStoppingCriteria=ctypes.POINTER(StoppingCriteria)
class CStoppingCriteria(ctypes_wrap.CStructWrapper):
    _struct=StoppingCriteria


class HighLevelParticleReport(ctypes.Structure):
    _fields_=[  ("area",ctypes.c_double),
                ("holeCount",ctypes.c_double),
                ("includeRect",RectDouble),
                ("centerMass",PointDouble),
                ("orientation",ctypes.c_double),
                ("dimensions",PointDouble) ]
PHighLevelParticleReport=ctypes.POINTER(HighLevelParticleReport)
class CHighLevelParticleReport(ctypes_wrap.CStructWrapper):
    _struct=HighLevelParticleReport


class HighLevelParticleAnalysisReport(ctypes.Structure):
    _fields_=[  ("numberOfParticles",ctypes.c_int),
                ("pixelReport",ctypes.POINTER(HighLevelParticleReport)),
                ("calibratedReport",ctypes.POINTER(HighLevelParticleReport)),
                ("calibrationValidity",ctypes.POINTER(ctypes.c_short)) ]
PHighLevelParticleAnalysisReport=ctypes.POINTER(HighLevelParticleAnalysisReport)
class CHighLevelParticleAnalysisReport(ctypes_wrap.CStructWrapper):
    _struct=HighLevelParticleAnalysisReport


class FlatFieldCorrectionOptions(ctypes.Structure):
    _fields_=[  ("correctionFactor",ctypes.c_float),
                ("lineScanImage",ctypes.c_int),
                ("optimizeCorrection",ctypes.c_int) ]
PFlatFieldCorrectionOptions=ctypes.POINTER(FlatFieldCorrectionOptions)
class CFlatFieldCorrectionOptions(ctypes_wrap.CStructWrapper):
    _struct=FlatFieldCorrectionOptions


class SurfaceFitOptions(ctypes.Structure):
    _fields_=[  ("gridWidth",ctypes.c_uint),
                ("gridHeight",ctypes.c_uint),
                ("polyDegree",ctypes.c_uint) ]
PSurfaceFitOptions=ctypes.POINTER(SurfaceFitOptions)
class CSurfaceFitOptions(ctypes_wrap.CStructWrapper):
    _struct=SurfaceFitOptions


class BackgroundEstimation(ctypes.Structure):
    _fields_=[  ("IsBackgroundEstimation",ctypes.c_uint),
                ("method",ctypes.c_int),
                ("polyDegree",ctypes.c_uint),
                ("windowWidth",ctypes.c_uint),
                ("windowHeight",ctypes.c_uint),
                ("devWeight",ctypes.c_double) ]
PBackgroundEstimation=ctypes.POINTER(BackgroundEstimation)
class CBackgroundEstimation(ctypes_wrap.CStructWrapper):
    _struct=BackgroundEstimation


class SVMKernelOptions(ctypes.Structure):
    _fields_=[  ("kernelType",ctypes.c_int),
                ("degree",ctypes.c_int),
                ("gamma",ctypes.c_double),
                ("coefficient",ctypes.c_double),
                ("sigma",ctypes.c_double),
                ("cacheSize",ctypes.c_double) ]
PSVMKernelOptions=ctypes.POINTER(SVMKernelOptions)
class CSVMKernelOptions(ctypes_wrap.CStructWrapper):
    _struct=SVMKernelOptions


class LabelWeight(ctypes.Structure):
    _fields_=[  ("label",ctypes.c_char_p),
                ("weight",ctypes.c_double) ]
PLabelWeight=ctypes.POINTER(LabelWeight)
class CLabelWeight(ctypes_wrap.CStructWrapper):
    _struct=LabelWeight


class SVMModelOptions(ctypes.Structure):
    _fields_=[  ("svmType",ctypes.c_int),
                ("epsilon",ctypes.c_double),
                ("maxIteration",ctypes.c_int),
                ("nu",ctypes.c_double),
                ("shrinking",ctypes.c_int),
                ("cost",ctypes.c_double),
                ("labelWeight",ctypes.POINTER(LabelWeight)),
                ("labelWeightCount",ctypes.c_int) ]
PSVMModelOptions=ctypes.POINTER(SVMModelOptions)
class CSVMModelOptions(ctypes_wrap.CStructWrapper):
    _struct=SVMModelOptions


class SVMTrainingResults(ctypes.Structure):
    _fields_=[  ("label",ctypes.c_char_p),
                ("stdDeviation",ctypes.c_float),
                ("count",ctypes.c_int),
                ("svCount",ctypes.c_int) ]
PSVMTrainingResults=ctypes.POINTER(SVMTrainingResults)
class CSVMTrainingResults(ctypes_wrap.CStructWrapper):
    _struct=SVMTrainingResults


class ClassDistanceTable(ctypes.Structure):
    _fields_=[  ("tableData",ctypes.POINTER(ctypes.c_float)),
                ("numOfRows",ctypes.c_int),
                ("numOfColumns",ctypes.c_int) ]
PClassDistanceTable=ctypes.POINTER(ClassDistanceTable)
class CClassDistanceTable(ctypes_wrap.CStructWrapper):
    _struct=ClassDistanceTable


class SVMReport(ctypes.Structure):
    _fields_=[  ("trainingResults",ctypes.POINTER(SVMTrainingResults)),
                ("SizeOftrainingResults",ctypes.c_uint),
                ("classDistanceTable",ctypes.POINTER(ClassDistanceTable)) ]
PSVMReport=ctypes.POINTER(SVMReport)
class CSVMReport(ctypes_wrap.CStructWrapper):
    _struct=SVMReport


class LearnContourSetupData(ctypes.Structure):
    _fields_=[  ("setupData",ctypes.c_char_p),
                ("setupDataLength",ctypes.c_uint) ]
PLearnContourSetupData=ctypes.POINTER(LearnContourSetupData)
class CLearnContourSetupData(ctypes_wrap.CStructWrapper):
    _struct=LearnContourSetupData


class PixelData(ctypes.Structure):
    _fields_=[  ("pixelPtr",ctypes.c_void_p),
                ("numOfPixels",ctypes.c_uint) ]
PPixelData=ctypes.POINTER(PixelData)
class CPixelData(ctypes_wrap.CStructWrapper):
    _struct=PixelData


class Palette(ctypes.Structure):
    _fields_=[  ("paletteData",ctypes.POINTER(RGBValue)),
                ("paletteDataLength",ctypes.c_uint) ]
PPalette=ctypes.POINTER(Palette)
class CPalette(ctypes_wrap.CStructWrapper):
    _struct=Palette


class ObjectDescription(ctypes.Structure):
    _fields_=[  ("label",ctypes.c_char_p),
                ("score",ctypes.c_int),
                ("angle",ctypes.c_double),
                ("location",PointDouble),
                ("boundingBox",ctypes.POINTER(PointDouble)),
                ("boundingBoxSize",ctypes.c_uint),
                ("objectFound",ctypes.c_int) ]
PObjectDescription=ctypes.POINTER(ObjectDescription)
class CObjectDescription(ctypes_wrap.CStructWrapper):
    _struct=ObjectDescription


class ObjectTrackingReport(ctypes.Structure):
    _fields_=[  ("numOfObjects",ctypes.c_uint),
                ("pixelDescription",ctypes.POINTER(ObjectDescription)),
                ("realObjectDescription",ctypes.POINTER(ObjectDescription)) ]
PObjectTrackingReport=ctypes.POINTER(ObjectTrackingReport)
class CObjectTrackingReport(ctypes_wrap.CStructWrapper):
    _struct=ObjectTrackingReport


class StereoCalibrationInfoReport(ctypes.Structure):
    _fields_=[  ("RotationMatrix",ctypes.POINTER(ctypes.c_double)),
                ("RotMRows",ctypes.c_uint),
                ("RotMCols",ctypes.c_uint),
                ("TranslationVector",ctypes.POINTER(ctypes.c_double)),
                ("NoTranslEle",ctypes.c_uint),
                ("EssentialMatrix",ctypes.POINTER(ctypes.c_double)),
                ("EsnMRows",ctypes.c_uint),
                ("EsnMCols",ctypes.c_uint),
                ("FundamentalMatrix",ctypes.POINTER(ctypes.c_double)),
                ("FndMRows",ctypes.c_uint),
                ("FndMCols",ctypes.c_uint),
                ("QMatrix",ctypes.POINTER(ctypes.c_double)),
                ("QMRows",ctypes.c_uint),
                ("QMCols",ctypes.c_uint) ]
PStereoCalibrationInfoReport=ctypes.POINTER(StereoCalibrationInfoReport)
class CStereoCalibrationInfoReport(ctypes_wrap.CStructWrapper):
    _struct=StereoCalibrationInfoReport


class Pixelto3dCoordinatesReport(ctypes.Structure):
    _fields_=[  ("RealCoordPt",StereoPointDbl3D),
                ("Real3DPoints",ctypes.POINTER(StereoPointDbl3D)),
                ("NumberofReal3DPoints",ctypes.c_uint),
                ("Real3DPtValidity",ctypes.c_int),
                ("Real3DPointsValidity",ctypes.POINTER(ctypes.c_int)),
                ("NumberofReal3DPtsVldt",ctypes.c_uint) ]
PPixelto3dCoordinatesReport=ctypes.POINTER(Pixelto3dCoordinatesReport)
class CPixelto3dCoordinatesReport(ctypes_wrap.CStructWrapper):
    _struct=Pixelto3dCoordinatesReport


class ImageToStringConversionReport(ctypes.Structure):
    _fields_=[  ("data",ctypes.c_char_p),
                ("dataLength",ctypes.c_uint) ]
PImageToStringConversionReport=ctypes.POINTER(ImageToStringConversionReport)
class CImageToStringConversionReport(ctypes_wrap.CStructWrapper):
    _struct=ImageToStringConversionReport


class OverlayGroupColor(ctypes.Structure):
    _fields_=[  ("groupName",ctypes.c_char_p),
                ("color",RGBValue),
                ("backgroundColor",RGBValue) ]
POverlayGroupColor=ctypes.POINTER(OverlayGroupColor)
class COverlayGroupColor(ctypes_wrap.CStructWrapper):
    _struct=OverlayGroupColor


EventCallback=ctypes.c_void_p



##### FUNCTION DEFINITIONS #####





def addfunc(lib, name, restype, argtypes=None, argnames=None):
    if getattr(lib,name,None) is None:
        setattr(lib,name,None)
    else:
        func=getattr(lib,name)
        func.restype=restype
        if argtypes is not None:
            func.argtypes=argtypes
        if argnames is not None:
            func.argnames=argnames

def define_functions(lib):
    #  ctypes.c_int imaqCast2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int type, ctypes.c_int method, ctypes.POINTER(ctypes.c_float) lookupTable, ctypes.c_int numberOfShift)
    addfunc(lib, "imaqCast2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int],
            argnames = ["dest", "source", "type", "method", "lookupTable", "numberOfShift"] )
    #  ctypes.c_int imaqCopyRect(ctypes.c_void_p dest, ctypes.c_void_p source, Rect rect, Point destLoc)
    addfunc(lib, "imaqCopyRect", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, Rect, Point],
            argnames = ["dest", "source", "rect", "destLoc"] )
    #  ctypes.c_int imaqDuplicate(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqDuplicate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqExtractTetragon(ctypes.c_void_p src, ctypes.c_void_p dest, ctypes.c_void_p roi, ctypes.POINTER(PointFloat) tetragon, ctypes.POINTER(ExtractTetragonOptions) options)
    addfunc(lib, "imaqExtractTetragon", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(PointFloat), ctypes.POINTER(ExtractTetragonOptions)],
            argnames = ["src", "dest", "roi", "tetragon", "options"] )
    #  ctypes.c_void_p imaqFlatten(ctypes.c_void_p image, ctypes.c_int type, ctypes.c_int compression, ctypes.c_int quality, ctypes.POINTER(ctypes.c_uint) size)
    addfunc(lib, "imaqFlatten", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "type", "compression", "quality", "size"] )
    #  ctypes.c_int imaqFlip(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int axis)
    addfunc(lib, "imaqFlip", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "axis"] )
    #  ctypes.POINTER(PixelData) imaqGetRowCol(ctypes.c_void_p image, ctypes.c_int index, ctypes.c_int isColumnIndex)
    addfunc(lib, "imaqGetRowCol", restype = ctypes.POINTER(PixelData),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["image", "index", "isColumnIndex"] )
    #  ctypes.c_int imaqMask(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_void_p mask)
    addfunc(lib, "imaqMask", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source", "mask"] )
    #  ctypes.c_int imaqResample(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int newWidth, ctypes.c_int newHeight, ctypes.c_int method, Rect rect)
    addfunc(lib, "imaqResample", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, Rect],
            argnames = ["dest", "source", "newWidth", "newHeight", "method", "rect"] )
    #  ctypes.c_int imaqRotate2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_float angle, ctypes.c_int fill, ctypes.c_int method, ctypes.c_int maintainSize)
    addfunc(lib, "imaqRotate2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "angle", "fill", "method", "maintainSize"] )
    #  ctypes.c_int imaqScale(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int xScale, ctypes.c_int yScale, ctypes.c_int scaleMode, Rect rect)
    addfunc(lib, "imaqScale", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, Rect],
            argnames = ["dest", "source", "xScale", "yScale", "scaleMode", "rect"] )
    #  ctypes.c_int imaqSetRowCol(ctypes.c_void_p image, ctypes.c_int index, ctypes.c_int isColumnIndex, ctypes.POINTER(PixelData) pixelData)
    addfunc(lib, "imaqSetRowCol", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(PixelData)],
            argnames = ["image", "index", "isColumnIndex", "pixelData"] )
    #  ctypes.c_int imaqShift(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int shiftX, ctypes.c_int shiftY, ctypes.c_int fill)
    addfunc(lib, "imaqShift", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "shiftX", "shiftY", "fill"] )
    #  ctypes.c_int imaqTranspose(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqTranspose", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqUnflatten(ctypes.c_void_p image, ctypes.c_void_p data, ctypes.c_uint size)
    addfunc(lib, "imaqUnflatten", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint],
            argnames = ["image", "data", "size"] )
    #  ctypes.c_int imaqUnwrapImage(ctypes.c_void_p dest, ctypes.c_void_p source, Annulus annulus, ctypes.c_int orientation, ctypes.c_int method)
    addfunc(lib, "imaqUnwrapImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, Annulus, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "annulus", "orientation", "method"] )
    #  ctypes.c_int imaqView3D(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(View3DOptions) options)
    addfunc(lib, "imaqView3D", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(View3DOptions)],
            argnames = ["dest", "source", "options"] )
    #  ctypes.c_int imaqAreToolsContextSensitive(ctypes.POINTER(ctypes.c_int) sensitive)
    addfunc(lib, "imaqAreToolsContextSensitive", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["sensitive"] )
    #  ctypes.c_int imaqCloseWindow(ctypes.c_int windowNumber)
    addfunc(lib, "imaqCloseWindow", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["windowNumber"] )
    #  ctypes.c_int imaqDisplayImage(ctypes.c_void_p image, ctypes.c_int windowNumber, ctypes.c_int resize)
    addfunc(lib, "imaqDisplayImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["image", "windowNumber", "resize"] )
    #  ctypes.c_int imaqGetLastKey(ctypes.c_char_p keyPressed, ctypes.POINTER(ctypes.c_int) windowNumber, ctypes.POINTER(ctypes.c_int) modifiers)
    addfunc(lib, "imaqGetLastKey", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["keyPressed", "windowNumber", "modifiers"] )
    #  ctypes.c_void_p imaqGetSystemWindowHandle(ctypes.c_int windowNumber)
    addfunc(lib, "imaqGetSystemWindowHandle", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_int],
            argnames = ["windowNumber"] )
    #  ctypes.c_int imaqGetWindowCenterPos(ctypes.c_int windowNumber, ctypes.POINTER(Point) centerPosition)
    addfunc(lib, "imaqGetWindowCenterPos", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(Point)],
            argnames = ["windowNumber", "centerPosition"] )
    #  ctypes.c_int imaqSetToolContextSensitivity(ctypes.c_int sensitive)
    addfunc(lib, "imaqSetToolContextSensitivity", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["sensitive"] )
    #  ctypes.c_int imaqShowWindow(ctypes.c_int windowNumber, ctypes.c_int visible)
    addfunc(lib, "imaqShowWindow", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["windowNumber", "visible"] )
    #  ctypes.c_int imaqCountParticles(ctypes.c_void_p image, ctypes.c_int connectivity8, ctypes.POINTER(ctypes.c_int) numParticles)
    addfunc(lib, "imaqCountParticles", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "connectivity8", "numParticles"] )
    #  ctypes.c_int imaqMeasureParticle(ctypes.c_void_p image, ctypes.c_int particleNumber, ctypes.c_int calibrated, ctypes.c_int measurement, ctypes.POINTER(ctypes.c_double) value)
    addfunc(lib, "imaqMeasureParticle", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double)],
            argnames = ["image", "particleNumber", "calibrated", "measurement", "value"] )
    #  ctypes.POINTER(MeasureParticlesReport) imaqMeasureParticles(ctypes.c_void_p image, ctypes.c_int calibrationMode, ctypes.POINTER(ctypes.c_int) measurements, ctypes.c_size_t numMeasurements)
    addfunc(lib, "imaqMeasureParticles", restype = ctypes.POINTER(MeasureParticlesReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.c_size_t],
            argnames = ["image", "calibrationMode", "measurements", "numMeasurements"] )
    #  ctypes.c_int imaqParticleFilter4(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ParticleFilterCriteria2) criteria, ctypes.c_int criteriaCount, ctypes.POINTER(ParticleFilterOptions2) options, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numParticles)
    addfunc(lib, "imaqParticleFilter4", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ParticleFilterCriteria2), ctypes.c_int, ctypes.POINTER(ParticleFilterOptions2), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "criteria", "criteriaCount", "options", "roi", "numParticles"] )
    #  ctypes.c_int imaqConvexHull(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int connectivity8)
    addfunc(lib, "imaqConvexHull", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "connectivity8"] )
    #  ctypes.c_int imaqDanielssonDistance(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqDanielssonDistance", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqFillHoles(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int connectivity8)
    addfunc(lib, "imaqFillHoles", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "connectivity8"] )
    #  ctypes.POINTER(CircleReport) imaqFindCircles(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_float minRadius, ctypes.c_float maxRadius, ctypes.POINTER(ctypes.c_int) numCircles)
    addfunc(lib, "imaqFindCircles", restype = ctypes.POINTER(CircleReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "minRadius", "maxRadius", "numCircles"] )
    #  ctypes.c_int imaqLabel2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int connectivity8, ctypes.POINTER(ctypes.c_int) particleCount)
    addfunc(lib, "imaqLabel2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "connectivity8", "particleCount"] )
    #  ctypes.c_int imaqMorphology(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int method, ctypes.POINTER(StructuringElement) structuringElement)
    addfunc(lib, "imaqMorphology", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(StructuringElement)],
            argnames = ["dest", "source", "method", "structuringElement"] )
    #  ctypes.c_int imaqRejectBorder(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int connectivity8)
    addfunc(lib, "imaqRejectBorder", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "connectivity8"] )
    #  ctypes.c_int imaqSegmentation(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqSegmentation", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqSeparation(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int erosions, ctypes.POINTER(StructuringElement) structuringElement)
    addfunc(lib, "imaqSeparation", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(StructuringElement)],
            argnames = ["dest", "source", "erosions", "structuringElement"] )
    #  ctypes.c_int imaqSimpleDistance(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(StructuringElement) structuringElement)
    addfunc(lib, "imaqSimpleDistance", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(StructuringElement)],
            argnames = ["dest", "source", "structuringElement"] )
    #  ctypes.c_int imaqSizeFilter(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int connectivity8, ctypes.c_int erosions, ctypes.c_int keepSize, ctypes.POINTER(StructuringElement) structuringElement)
    addfunc(lib, "imaqSizeFilter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(StructuringElement)],
            argnames = ["dest", "source", "connectivity8", "erosions", "keepSize", "structuringElement"] )
    #  ctypes.c_int imaqSkeleton(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int method)
    addfunc(lib, "imaqSkeleton", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "method"] )
    #  ctypes.c_void_p imaqCopyFromRing(SESSION_ID sessionID, ctypes.c_void_p image, ctypes.c_int imageToCopy, ctypes.POINTER(ctypes.c_int) imageNumber, Rect rect)
    addfunc(lib, "imaqCopyFromRing", restype = ctypes.c_void_p,
            argtypes = [SESSION_ID, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), Rect],
            argnames = ["sessionID", "image", "imageToCopy", "imageNumber", "rect"] )
    #  ctypes.c_void_p imaqEasyAcquire(ctypes.c_char_p interfaceName)
    addfunc(lib, "imaqEasyAcquire", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_char_p],
            argnames = ["interfaceName"] )
    #  ctypes.c_void_p imaqExtractFromRing(SESSION_ID sessionID, ctypes.c_int imageToExtract, ctypes.POINTER(ctypes.c_int) imageNumber)
    addfunc(lib, "imaqExtractFromRing", restype = ctypes.c_void_p,
            argtypes = [SESSION_ID, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["sessionID", "imageToExtract", "imageNumber"] )
    #  ctypes.c_void_p imaqGrab(SESSION_ID sessionID, ctypes.c_void_p image, ctypes.c_int immediate)
    addfunc(lib, "imaqGrab", restype = ctypes.c_void_p,
            argtypes = [SESSION_ID, ctypes.c_void_p, ctypes.c_int],
            argnames = ["sessionID", "image", "immediate"] )
    #  ctypes.c_int imaqReleaseImage(SESSION_ID sessionID)
    addfunc(lib, "imaqReleaseImage", restype = ctypes.c_int,
            argtypes = [SESSION_ID],
            argnames = ["sessionID"] )
    #  ctypes.c_int imaqSetupGrab(SESSION_ID sessionID, Rect rect)
    addfunc(lib, "imaqSetupGrab", restype = ctypes.c_int,
            argtypes = [SESSION_ID, Rect],
            argnames = ["sessionID", "rect"] )
    #  ctypes.c_int imaqSetupRing(SESSION_ID sessionID, ctypes.POINTER(ctypes.c_void_p) images, ctypes.c_int numImages, ctypes.c_int skipCount, Rect rect)
    addfunc(lib, "imaqSetupRing", restype = ctypes.c_int,
            argtypes = [SESSION_ID, ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_int, Rect],
            argnames = ["sessionID", "images", "numImages", "skipCount", "rect"] )
    #  ctypes.c_int imaqSetupSequence(SESSION_ID sessionID, ctypes.POINTER(ctypes.c_void_p) images, ctypes.c_int numImages, ctypes.c_int skipCount, Rect rect)
    addfunc(lib, "imaqSetupSequence", restype = ctypes.c_int,
            argtypes = [SESSION_ID, ctypes.POINTER(ctypes.c_void_p), ctypes.c_int, ctypes.c_int, Rect],
            argnames = ["sessionID", "images", "numImages", "skipCount", "rect"] )
    #  ctypes.c_void_p imaqSnap(SESSION_ID sessionID, ctypes.c_void_p image, Rect rect)
    addfunc(lib, "imaqSnap", restype = ctypes.c_void_p,
            argtypes = [SESSION_ID, ctypes.c_void_p, Rect],
            argnames = ["sessionID", "image", "rect"] )
    #  ctypes.c_int imaqStartAcquisition(SESSION_ID sessionID)
    addfunc(lib, "imaqStartAcquisition", restype = ctypes.c_int,
            argtypes = [SESSION_ID],
            argnames = ["sessionID"] )
    #  ctypes.c_int imaqStopAcquisition(SESSION_ID sessionID)
    addfunc(lib, "imaqStopAcquisition", restype = ctypes.c_int,
            argtypes = [SESSION_ID],
            argnames = ["sessionID"] )
    #  ctypes.c_int imaqAbsoluteDifference(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqAbsoluteDifference", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqAbsoluteDifferenceConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqAbsoluteDifferenceConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqAdd(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqAdd", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqAddConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqAddConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqAverage(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqAverage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqAverageConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqAverageConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqDivide2(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB, ctypes.c_int roundingMode)
    addfunc(lib, "imaqDivide2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "sourceA", "sourceB", "roundingMode"] )
    #  ctypes.c_int imaqDivideConstant2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value, ctypes.c_int roundingMode)
    addfunc(lib, "imaqDivideConstant2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "value", "roundingMode"] )
    #  ctypes.c_int imaqMax(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqMax", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqMaxConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqMaxConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqMin(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqMin", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqMinConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqMinConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqModulo(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqModulo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqModuloConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqModuloConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqMulDiv(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB, ctypes.c_float value)
    addfunc(lib, "imaqMulDiv", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float],
            argnames = ["dest", "sourceA", "sourceB", "value"] )
    #  ctypes.c_int imaqMultiply(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqMultiply", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqMultiplyConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqMultiplyConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqSubtract(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqSubtract", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqSubtractConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqSubtractConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.POINTER(CaliperReport) imaqCaliperTool(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.POINTER(EdgeOptions) edgeOptions, ctypes.POINTER(CaliperOptions) caliperOptions, ctypes.POINTER(ctypes.c_int) numEdgePairs)
    addfunc(lib, "imaqCaliperTool", restype = ctypes.POINTER(CaliperReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(EdgeOptions), ctypes.POINTER(CaliperOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "points", "numPoints", "edgeOptions", "caliperOptions", "numEdgePairs"] )
    #  ctypes.POINTER(ConcentricRakeReport2) imaqConcentricRake3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.c_int optimizedMode, ctypes.c_int stepSize, ctypes.POINTER(EdgeOptions2) edgeOptions)
    addfunc(lib, "imaqConcentricRake3", restype = ctypes.POINTER(ConcentricRakeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(EdgeOptions2)],
            argnames = ["image", "roi", "direction", "process", "optimizedMode", "stepSize", "edgeOptions"] )
    #  ctypes.POINTER(ExtremeReport) imaqDetectExtremes(ctypes.POINTER(ctypes.c_double) pixels, ctypes.c_int numPixels, ctypes.c_int mode, ctypes.POINTER(DetectExtremesOptions) options, ctypes.POINTER(ctypes.c_int) numExtremes)
    addfunc(lib, "imaqDetectExtremes", restype = ctypes.POINTER(ExtremeReport),
            argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int, ctypes.c_int, ctypes.POINTER(DetectExtremesOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["pixels", "numPixels", "mode", "options", "numExtremes"] )
    #  ctypes.c_int imaqDetectRotation(ctypes.c_void_p referenceImage, ctypes.c_void_p testImage, PointFloat referenceCenter, PointFloat testCenter, ctypes.c_int radius, ctypes.c_float precision, ctypes.POINTER(ctypes.c_double) angle)
    addfunc(lib, "imaqDetectRotation", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, PointFloat, PointFloat, ctypes.c_int, ctypes.c_float, ctypes.POINTER(ctypes.c_double)],
            argnames = ["referenceImage", "testImage", "referenceCenter", "testCenter", "radius", "precision", "angle"] )
    #  ctypes.POINTER(EdgeReport2) imaqEdgeTool4(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int processType, ctypes.POINTER(EdgeOptions2) edgeOptions, ctypes.c_uint reverseDirection)
    addfunc(lib, "imaqEdgeTool4", restype = ctypes.POINTER(EdgeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(EdgeOptions2), ctypes.c_uint],
            argnames = ["image", "roi", "processType", "edgeOptions", "reverseDirection"] )
    #  ctypes.POINTER(FindEdgeReport) imaqFindEdge2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(FindEdgeOptions2) findEdgeOptions, ctypes.POINTER(StraightEdgeOptions) straightEdgeOptions)
    addfunc(lib, "imaqFindEdge2", restype = ctypes.POINTER(FindEdgeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(FindEdgeOptions2), ctypes.POINTER(StraightEdgeOptions)],
            argnames = ["image", "roi", "baseSystem", "newSystem", "findEdgeOptions", "straightEdgeOptions"] )
    #  ctypes.POINTER(FindEdgeReport) imaqFindEdge3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(FindEdgeOptions2) findEdgeOptions, ctypes.POINTER(StraightEdgeOptions) straightEdgeOptions)
    addfunc(lib, "imaqFindEdge3", restype = ctypes.POINTER(FindEdgeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(FindEdgeOptions2), ctypes.POINTER(StraightEdgeOptions)],
            argnames = ["image", "roi", "baseSystem", "newSystem", "findEdgeOptions", "straightEdgeOptions"] )
    #  ctypes.c_int imaqFindTransformRect2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int mode, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(FindTransformRectOptions2) findTransformOptions, ctypes.POINTER(StraightEdgeOptions) straightEdgeOptions, ctypes.POINTER(AxisReport) axisReport)
    addfunc(lib, "imaqFindTransformRect2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(FindTransformRectOptions2), ctypes.POINTER(StraightEdgeOptions), ctypes.POINTER(AxisReport)],
            argnames = ["image", "roi", "mode", "baseSystem", "newSystem", "findTransformOptions", "straightEdgeOptions", "axisReport"] )
    #  ctypes.c_int imaqFindTransformRects2(ctypes.c_void_p image, ctypes.c_void_p primaryROI, ctypes.c_void_p secondaryROI, ctypes.c_int mode, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(FindTransformRectsOptions2) findTransformOptions, ctypes.POINTER(StraightEdgeOptions) primaryStraightEdgeOptions, ctypes.POINTER(StraightEdgeOptions) secondaryStraightEdgeOptions, ctypes.POINTER(AxisReport) axisReport)
    addfunc(lib, "imaqFindTransformRects2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(FindTransformRectsOptions2), ctypes.POINTER(StraightEdgeOptions), ctypes.POINTER(StraightEdgeOptions), ctypes.POINTER(AxisReport)],
            argnames = ["image", "primaryROI", "secondaryROI", "mode", "baseSystem", "newSystem", "findTransformOptions", "primaryStraightEdgeOptions", "secondaryStraightEdgeOptions", "axisReport"] )
    #  ctypes.c_int imaqLineGaugeTool2(ctypes.c_void_p image, Point start, Point end, ctypes.c_int method, ctypes.POINTER(EdgeOptions) edgeOptions, ctypes.POINTER(CoordinateTransform2) transform, ctypes.POINTER(ctypes.c_float) distance)
    addfunc(lib, "imaqLineGaugeTool2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, Point, ctypes.c_int, ctypes.POINTER(EdgeOptions), ctypes.POINTER(CoordinateTransform2), ctypes.POINTER(ctypes.c_float)],
            argnames = ["image", "start", "end", "method", "edgeOptions", "transform", "distance"] )
    #  ctypes.POINTER(RakeReport2) imaqRake3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.c_int optimizedMode, ctypes.c_int stepSize, ctypes.POINTER(EdgeOptions2) edgeOptions)
    addfunc(lib, "imaqRake3", restype = ctypes.POINTER(RakeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(EdgeOptions2)],
            argnames = ["image", "roi", "direction", "process", "optimizedMode", "stepSize", "edgeOptions"] )
    #  ctypes.POINTER(PointFloat) imaqSimpleEdge(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.POINTER(SimpleEdgeOptions) options, ctypes.POINTER(ctypes.c_int) numEdges)
    addfunc(lib, "imaqSimpleEdge", restype = ctypes.POINTER(PointFloat),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(SimpleEdgeOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "points", "numPoints", "options", "numEdges"] )
    #  ctypes.POINTER(SpokeReport2) imaqSpoke3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.c_int optimizedMode, ctypes.c_int stepSize, ctypes.POINTER(EdgeOptions2) edgeOptions)
    addfunc(lib, "imaqSpoke3", restype = ctypes.POINTER(SpokeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(EdgeOptions2)],
            argnames = ["image", "roi", "direction", "process", "optimizedMode", "stepSize", "edgeOptions"] )
    #  ctypes.POINTER(StraightEdgeReport2) imaqStraightEdge(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int searchDirection, ctypes.POINTER(EdgeOptions2) edgeOptions, ctypes.POINTER(StraightEdgeOptions) straightEdgeOptions)
    addfunc(lib, "imaqStraightEdge", restype = ctypes.POINTER(StraightEdgeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(EdgeOptions2), ctypes.POINTER(StraightEdgeOptions)],
            argnames = ["image", "roi", "searchDirection", "edgeOptions", "straightEdgeOptions"] )
    #  ctypes.POINTER(StraightEdgeReport2) imaqStraightEdge2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int searchDirection, ctypes.POINTER(EdgeOptions2) edgeOptions, ctypes.POINTER(StraightEdgeOptions) straightEdgeOptions, ctypes.c_uint optimizedMode)
    addfunc(lib, "imaqStraightEdge2", restype = ctypes.POINTER(StraightEdgeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(EdgeOptions2), ctypes.POINTER(StraightEdgeOptions), ctypes.c_uint],
            argnames = ["image", "roi", "searchDirection", "edgeOptions", "straightEdgeOptions", "optimizedMode"] )
    #  ctypes.POINTER(StraightEdgeReport2) imaqStraightEdge3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int searchDirection, ctypes.POINTER(EdgeOptions2) edgeOptions, ctypes.POINTER(StraightEdgeOptions) straightEdgeOptions, ctypes.c_uint optimizedMode)
    addfunc(lib, "imaqStraightEdge3", restype = ctypes.POINTER(StraightEdgeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(EdgeOptions2), ctypes.POINTER(StraightEdgeOptions), ctypes.c_uint],
            argnames = ["image", "roi", "searchDirection", "edgeOptions", "straightEdgeOptions", "optimizedMode"] )
    #  ctypes.c_int imaqCannyEdgeFilter(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(CannyOptions) options)
    addfunc(lib, "imaqCannyEdgeFilter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CannyOptions)],
            argnames = ["dest", "source", "options"] )
    #  ctypes.c_int imaqConvolve2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ctypes.c_float) kernel, ctypes.c_int matrixRows, ctypes.c_int matrixCols, ctypes.c_float normalize, ctypes.c_void_p mask, ctypes.c_int roundingMode)
    addfunc(lib, "imaqConvolve2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "kernel", "matrixRows", "matrixCols", "normalize", "mask", "roundingMode"] )
    #  ctypes.c_int imaqCorrelate(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_void_p templateImage, Rect rect)
    addfunc(lib, "imaqCorrelate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, Rect],
            argnames = ["dest", "source", "templateImage", "rect"] )
    #  ctypes.c_int imaqEdgeFilter(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int method, ctypes.c_void_p mask)
    addfunc(lib, "imaqEdgeFilter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p],
            argnames = ["dest", "source", "method", "mask"] )
    #  ctypes.c_int imaqLowPass(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int width, ctypes.c_int height, ctypes.c_float tolerance, ctypes.c_void_p mask)
    addfunc(lib, "imaqLowPass", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_void_p],
            argnames = ["dest", "source", "width", "height", "tolerance", "mask"] )
    #  ctypes.c_int imaqMedianFilter(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int width, ctypes.c_int height, ctypes.c_void_p mask)
    addfunc(lib, "imaqMedianFilter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p],
            argnames = ["dest", "source", "width", "height", "mask"] )
    #  ctypes.c_int imaqNthOrderFilter(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int width, ctypes.c_int height, ctypes.c_int n, ctypes.c_void_p mask)
    addfunc(lib, "imaqNthOrderFilter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p],
            argnames = ["dest", "source", "width", "height", "n", "mask"] )
    #  ctypes.c_int imaqDrawLineOnImage(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int mode, Point start, Point end, ctypes.c_float newPixelValue)
    addfunc(lib, "imaqDrawLineOnImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, Point, Point, ctypes.c_float],
            argnames = ["dest", "source", "mode", "start", "end", "newPixelValue"] )
    #  ctypes.c_int imaqDrawShapeOnImage(ctypes.c_void_p dest, ctypes.c_void_p source, Rect rect, ctypes.c_int mode, ctypes.c_int shape, ctypes.c_float newPixelValue)
    addfunc(lib, "imaqDrawShapeOnImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, Rect, ctypes.c_int, ctypes.c_int, ctypes.c_float],
            argnames = ["dest", "source", "rect", "mode", "shape", "newPixelValue"] )
    #  ctypes.c_int imaqDrawTextOnImage(ctypes.c_void_p dest, ctypes.c_void_p source, Point coord, ctypes.c_char_p text, ctypes.POINTER(DrawTextOptions) options, ctypes.POINTER(ctypes.c_int) fontNameUsed)
    addfunc(lib, "imaqDrawTextOnImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, Point, ctypes.c_char_p, ctypes.POINTER(DrawTextOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "coord", "text", "options", "fontNameUsed"] )
    #  ctypes.c_int imaqInterlaceCombine(ctypes.c_void_p frame, ctypes.c_void_p odd, ctypes.c_void_p even)
    addfunc(lib, "imaqInterlaceCombine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["frame", "odd", "even"] )
    #  ctypes.c_int imaqInterlaceSeparate(ctypes.c_void_p frame, ctypes.c_void_p odd, ctypes.c_void_p even)
    addfunc(lib, "imaqInterlaceSeparate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["frame", "odd", "even"] )
    #  ctypes.c_int imaqAttenuate(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int highlow)
    addfunc(lib, "imaqAttenuate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "highlow"] )
    #  ctypes.c_int imaqConjugate(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqConjugate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqFFT(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqFFT", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqFlipFrequencies(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqFlipFrequencies", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqInverseFFT(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqInverseFFT", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqTruncate(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int highlow, ctypes.c_float ratioToKeep)
    addfunc(lib, "imaqTruncate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_float],
            argnames = ["dest", "source", "highlow", "ratioToKeep"] )
    #  ctypes.c_int imaqCloseToolWindow()
    addfunc(lib, "imaqCloseToolWindow", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int imaqGetCurrentTool(ctypes.POINTER(ctypes.c_int) currentTool)
    addfunc(lib, "imaqGetCurrentTool", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["currentTool"] )
    #  ctypes.c_int imaqGetLastEvent(ctypes.POINTER(ctypes.c_int) type, ctypes.POINTER(ctypes.c_int) windowNumber, ctypes.POINTER(ctypes.c_int) tool, ctypes.POINTER(Rect) rect)
    addfunc(lib, "imaqGetLastEvent", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(Rect)],
            argnames = ["type", "windowNumber", "tool", "rect"] )
    #  ctypes.c_void_p imaqGetToolWindowHandle()
    addfunc(lib, "imaqGetToolWindowHandle", restype = ctypes.c_void_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int imaqGetToolWindowPos(ctypes.POINTER(Point) position)
    addfunc(lib, "imaqGetToolWindowPos", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(Point)],
            argnames = ["position"] )
    #  ctypes.c_int imaqIsToolWindowVisible(ctypes.POINTER(ctypes.c_int) visible)
    addfunc(lib, "imaqIsToolWindowVisible", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["visible"] )
    #  ctypes.c_int imaqMoveToolWindow(Point position)
    addfunc(lib, "imaqMoveToolWindow", restype = ctypes.c_int,
            argtypes = [Point],
            argnames = ["position"] )
    #  ctypes.c_int imaqSetCurrentTool(ctypes.c_int currentTool)
    addfunc(lib, "imaqSetCurrentTool", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["currentTool"] )
    #  ctypes.c_int imaqSetEventCallback(EventCallback callback, ctypes.c_int synchronous)
    addfunc(lib, "imaqSetEventCallback", restype = ctypes.c_int,
            argtypes = [EventCallback, ctypes.c_int],
            argnames = ["callback", "synchronous"] )
    #  ctypes.c_int imaqSetToolColor(ctypes.POINTER(RGBValue) color)
    addfunc(lib, "imaqSetToolColor", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(RGBValue)],
            argnames = ["color"] )
    #  ctypes.c_int imaqSetupToolWindow(ctypes.c_int showCoordinates, ctypes.c_int maxIconsPerLine, ctypes.POINTER(ToolWindowOptions) options)
    addfunc(lib, "imaqSetupToolWindow", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ToolWindowOptions)],
            argnames = ["showCoordinates", "maxIconsPerLine", "options"] )
    #  ctypes.c_int imaqShowToolWindow(ctypes.c_int visible)
    addfunc(lib, "imaqShowToolWindow", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["visible"] )
    #  ctypes.c_int imaqGetFileInfo(ctypes.c_char_p fileName, ctypes.POINTER(ctypes.c_int) calibrationUnit, ctypes.POINTER(ctypes.c_float) calibrationX, ctypes.POINTER(ctypes.c_float) calibrationY, ctypes.POINTER(ctypes.c_int) width, ctypes.POINTER(ctypes.c_int) height, ctypes.POINTER(ctypes.c_int) imageType)
    addfunc(lib, "imaqGetFileInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["fileName", "calibrationUnit", "calibrationX", "calibrationY", "width", "height", "imageType"] )
    #  ctypes.POINTER(ctypes.c_char_p) imaqLoadImagePopup(ctypes.c_char_p defaultDirectory, ctypes.c_char_p defaultFileSpec, ctypes.c_char_p fileTypeList, ctypes.c_char_p title, ctypes.c_int allowMultiplePaths, ctypes.c_int buttonLabel, ctypes.c_int restrictDirectory, ctypes.c_int restrictExtension, ctypes.c_int allowCancel, ctypes.c_int allowMakeDirectory, ctypes.POINTER(ctypes.c_int) cancelled, ctypes.POINTER(ctypes.c_int) numPaths)
    addfunc(lib, "imaqLoadImagePopup", restype = ctypes.POINTER(ctypes.c_char_p),
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["defaultDirectory", "defaultFileSpec", "fileTypeList", "title", "allowMultiplePaths", "buttonLabel", "restrictDirectory", "restrictExtension", "allowCancel", "allowMakeDirectory", "cancelled", "numPaths"] )
    #  ctypes.c_int imaqReadFile2(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.c_int imageTypeSrc, ctypes.POINTER(RGBValue) colorTable, ctypes.POINTER(ctypes.c_int) numColors)
    addfunc(lib, "imaqReadFile2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "fileName", "imageTypeSrc", "colorTable", "numColors"] )
    #  ctypes.c_int imaqReadVisionFile2(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.c_int imageTypeSrc, ctypes.POINTER(RGBValue) colorTable, ctypes.POINTER(ctypes.c_int) numColors)
    addfunc(lib, "imaqReadVisionFile2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "fileName", "imageTypeSrc", "colorTable", "numColors"] )
    #  ctypes.c_int imaqWriteBMPFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.c_int compress, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteBMPFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(RGBValue)],
            argnames = ["image", "fileName", "compress", "colorTable"] )
    #  ctypes.c_int imaqWriteFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(RGBValue)],
            argnames = ["image", "fileName", "colorTable"] )
    #  ctypes.c_int imaqWriteJPEGFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.c_uint quality, ctypes.c_void_p colorTable)
    addfunc(lib, "imaqWriteJPEGFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint, ctypes.c_void_p],
            argnames = ["image", "fileName", "quality", "colorTable"] )
    #  ctypes.c_int imaqWriteJPEG2000File(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.c_int lossless, ctypes.c_float compressionRatio, ctypes.POINTER(JPEG2000FileAdvancedOptions) advancedOptions, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteJPEG2000File", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_float, ctypes.POINTER(JPEG2000FileAdvancedOptions), ctypes.POINTER(RGBValue)],
            argnames = ["image", "fileName", "lossless", "compressionRatio", "advancedOptions", "colorTable"] )
    #  ctypes.c_int imaqWritePNGFile2(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.c_uint compressionSpeed, ctypes.POINTER(RGBValue) colorTable, ctypes.c_int useBitDepth)
    addfunc(lib, "imaqWritePNGFile2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint, ctypes.POINTER(RGBValue), ctypes.c_int],
            argnames = ["image", "fileName", "compressionSpeed", "colorTable", "useBitDepth"] )
    #  ctypes.c_int imaqWriteTIFFFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.POINTER(TIFFFileOptions) options, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteTIFFFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(TIFFFileOptions), ctypes.POINTER(RGBValue)],
            argnames = ["image", "fileName", "options", "colorTable"] )
    #  ctypes.c_int imaqWriteVisionFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteVisionFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(RGBValue)],
            argnames = ["image", "fileName", "colorTable"] )
    #  ctypes.POINTER(FilterName) imaqGetFilterNames2(ctypes.c_void_p image, ctypes.c_int codecType, ctypes.POINTER(ctypes.c_int) numFilters)
    addfunc(lib, "imaqGetFilterNames2", restype = ctypes.POINTER(FilterName),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "codecType", "numFilters"] )
    #  AVI2Session imaqCreateAVI2(ctypes.c_char_p filename, ctypes.c_char_p compressionFilter, ctypes.c_int quality, ctypes.c_uint framesPerSecond)
    addfunc(lib, "imaqCreateAVI2", restype = AVI2Session,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint],
            argnames = ["filename", "compressionFilter", "quality", "framesPerSecond"] )
    #  ctypes.c_int imaqWriteAVIFrame2(ctypes.c_void_p image, AVI2Session avi2Session)
    addfunc(lib, "imaqWriteAVIFrame2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, AVI2Session],
            argnames = ["image", "avi2Session"] )
    #  AVI2Session imaqOpenAVI2(ctypes.c_char_p fileName, ctypes.c_int codecType)
    addfunc(lib, "imaqOpenAVI2", restype = AVI2Session,
            argtypes = [ctypes.c_char_p, ctypes.c_int],
            argnames = ["fileName", "codecType"] )
    #  ctypes.c_int imaqReadAVIFrame2(ctypes.c_void_p image, AVI2Session avi2Session, ctypes.c_int frameNumber)
    addfunc(lib, "imaqReadAVIFrame2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, AVI2Session, ctypes.c_int],
            argnames = ["image", "avi2Session", "frameNumber"] )
    #  ctypes.c_int imaqGetAVIInfo2(AVI2Session avi2Session, ctypes.POINTER(AVIInfo) aviInfo)
    addfunc(lib, "imaqGetAVIInfo2", restype = ctypes.c_int,
            argtypes = [AVI2Session, ctypes.POINTER(AVIInfo)],
            argnames = ["avi2Session", "aviInfo"] )
    #  ctypes.c_int imaqCloseAVI2(AVI2Session avi2Session)
    addfunc(lib, "imaqCloseAVI2", restype = ctypes.c_int,
            argtypes = [AVI2Session],
            argnames = ["avi2Session"] )
    #  ctypes.c_int imaqAnd(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqAnd", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqAndConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqAndConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqCompare(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_void_p compareImage, ctypes.c_int compare)
    addfunc(lib, "imaqCompare", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "compareImage", "compare"] )
    #  ctypes.c_int imaqCompareConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value, ctypes.c_int compare)
    addfunc(lib, "imaqCompareConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "value", "compare"] )
    #  ctypes.c_int imaqLogicalDifference(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqLogicalDifference", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqLogicalDifferenceConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqLogicalDifferenceConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqNand(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqNand", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqNandConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqNandConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqNor(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqNor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqNorConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqNorConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqOr(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqOr", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqOrConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqOrConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqXnor(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqXnor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqXnorConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqXnorConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqXor(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqXor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqXorConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqXorConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqBuildCoordinateSystem(ctypes.POINTER(Point) points, ctypes.c_int mode, ctypes.c_int orientation, ctypes.POINTER(CoordinateSystem) system)
    addfunc(lib, "imaqBuildCoordinateSystem", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(Point), ctypes.c_int, ctypes.c_int, ctypes.POINTER(CoordinateSystem)],
            argnames = ["points", "mode", "orientation", "system"] )
    #  ctypes.POINTER(BestCircle2) imaqFitCircle2(ctypes.POINTER(PointFloat) points, ctypes.c_int numPoints, ctypes.POINTER(FitCircleOptions) options)
    addfunc(lib, "imaqFitCircle2", restype = ctypes.POINTER(BestCircle2),
            argtypes = [ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.POINTER(FitCircleOptions)],
            argnames = ["points", "numPoints", "options"] )
    #  ctypes.POINTER(BestEllipse2) imaqFitEllipse2(ctypes.POINTER(PointFloat) points, ctypes.c_int numPoints, ctypes.POINTER(FitEllipseOptions) options)
    addfunc(lib, "imaqFitEllipse2", restype = ctypes.POINTER(BestEllipse2),
            argtypes = [ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.POINTER(FitEllipseOptions)],
            argnames = ["points", "numPoints", "options"] )
    #  ctypes.POINTER(BestLine) imaqFitLine(ctypes.POINTER(PointFloat) points, ctypes.c_int numPoints, ctypes.POINTER(FitLineOptions) options)
    addfunc(lib, "imaqFitLine", restype = ctypes.POINTER(BestLine),
            argtypes = [ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.POINTER(FitLineOptions)],
            argnames = ["points", "numPoints", "options"] )
    #  ctypes.c_int imaqGetAngle(PointFloat start1, PointFloat end1, PointFloat start2, PointFloat end2, ctypes.POINTER(ctypes.c_float) angle)
    addfunc(lib, "imaqGetAngle", restype = ctypes.c_int,
            argtypes = [PointFloat, PointFloat, PointFloat, PointFloat, ctypes.POINTER(ctypes.c_float)],
            argnames = ["start1", "end1", "start2", "end2", "angle"] )
    #  ctypes.c_int imaqGetBisectingLine(PointFloat start1, PointFloat end1, PointFloat start2, PointFloat end2, ctypes.POINTER(PointFloat) bisectStart, ctypes.POINTER(PointFloat) bisectEnd)
    addfunc(lib, "imaqGetBisectingLine", restype = ctypes.c_int,
            argtypes = [PointFloat, PointFloat, PointFloat, PointFloat, ctypes.POINTER(PointFloat), ctypes.POINTER(PointFloat)],
            argnames = ["start1", "end1", "start2", "end2", "bisectStart", "bisectEnd"] )
    #  ctypes.c_int imaqGetDistance(PointFloat point1, PointFloat point2, ctypes.POINTER(ctypes.c_float) distance)
    addfunc(lib, "imaqGetDistance", restype = ctypes.c_int,
            argtypes = [PointFloat, PointFloat, ctypes.POINTER(ctypes.c_float)],
            argnames = ["point1", "point2", "distance"] )
    #  ctypes.c_int imaqGetIntersection(PointFloat start1, PointFloat end1, PointFloat start2, PointFloat end2, ctypes.POINTER(PointFloat) intersection)
    addfunc(lib, "imaqGetIntersection", restype = ctypes.c_int,
            argtypes = [PointFloat, PointFloat, PointFloat, PointFloat, ctypes.POINTER(PointFloat)],
            argnames = ["start1", "end1", "start2", "end2", "intersection"] )
    #  ctypes.c_int imaqGetMidLine(PointFloat refLineStart, PointFloat refLineEnd, PointFloat point, ctypes.POINTER(PointFloat) midLineStart, ctypes.POINTER(PointFloat) midLineEnd)
    addfunc(lib, "imaqGetMidLine", restype = ctypes.c_int,
            argtypes = [PointFloat, PointFloat, PointFloat, ctypes.POINTER(PointFloat), ctypes.POINTER(PointFloat)],
            argnames = ["refLineStart", "refLineEnd", "point", "midLineStart", "midLineEnd"] )
    #  ctypes.c_int imaqGetPerpendicularLine(PointFloat refLineStart, PointFloat refLineEnd, PointFloat point, ctypes.POINTER(PointFloat) perpLineStart, ctypes.POINTER(PointFloat) perpLineEnd, ctypes.POINTER(ctypes.c_double) distance)
    addfunc(lib, "imaqGetPerpendicularLine", restype = ctypes.c_int,
            argtypes = [PointFloat, PointFloat, PointFloat, ctypes.POINTER(PointFloat), ctypes.POINTER(PointFloat), ctypes.POINTER(ctypes.c_double)],
            argnames = ["refLineStart", "refLineEnd", "point", "perpLineStart", "perpLineEnd", "distance"] )
    #  ctypes.POINTER(SegmentInfo) imaqGetPointsOnContour(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_int) numSegments)
    addfunc(lib, "imaqGetPointsOnContour", restype = ctypes.POINTER(SegmentInfo),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "numSegments"] )
    #  ctypes.POINTER(Point) imaqGetPointsOnLine(Point start, Point end, ctypes.POINTER(ctypes.c_int) numPoints)
    addfunc(lib, "imaqGetPointsOnLine", restype = ctypes.POINTER(Point),
            argtypes = [Point, Point, ctypes.POINTER(ctypes.c_int)],
            argnames = ["start", "end", "numPoints"] )
    #  ctypes.c_int imaqGetPolygonArea(ctypes.POINTER(PointFloat) points, ctypes.c_int numPoints, ctypes.POINTER(ctypes.c_float) area)
    addfunc(lib, "imaqGetPolygonArea", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["points", "numPoints", "area"] )
    #  ctypes.POINTER(ctypes.c_float) imaqInterpolatePoints(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.c_int method, ctypes.c_int subpixel, ctypes.POINTER(ctypes.c_int) interpCount)
    addfunc(lib, "imaqInterpolatePoints", restype = ctypes.POINTER(ctypes.c_float),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "points", "numPoints", "method", "subpixel", "interpCount"] )
    #  ctypes.c_int imaqClipboardToImage(ctypes.c_void_p dest, ctypes.POINTER(RGBValue) palette)
    addfunc(lib, "imaqClipboardToImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(RGBValue)],
            argnames = ["dest", "palette"] )
    #  ctypes.c_int imaqImageToClipboard(ctypes.c_void_p image, ctypes.POINTER(RGBValue) palette)
    addfunc(lib, "imaqImageToClipboard", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(RGBValue)],
            argnames = ["image", "palette"] )
    #  ctypes.c_int imaqFillBorder(ctypes.c_void_p image, ctypes.c_int method)
    addfunc(lib, "imaqFillBorder", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["image", "method"] )
    #  ctypes.c_int imaqGetBorderSize(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_int) borderSize)
    addfunc(lib, "imaqGetBorderSize", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "borderSize"] )
    #  ctypes.c_int imaqSetBorderSize(ctypes.c_void_p image, ctypes.c_int size)
    addfunc(lib, "imaqSetBorderSize", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["image", "size"] )
    #  ctypes.c_int imaqArrayToImage(ctypes.c_void_p image, ctypes.c_void_p array, ctypes.c_int numCols, ctypes.c_int numRows)
    addfunc(lib, "imaqArrayToImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["image", "array", "numCols", "numRows"] )
    #  ctypes.c_void_p imaqCreateImage(ctypes.c_int type, ctypes.c_int borderSize)
    addfunc(lib, "imaqCreateImage", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["type", "borderSize"] )
    #  ctypes.c_void_p imaqImageToArray(ctypes.c_void_p image, Rect rect, ctypes.POINTER(ctypes.c_int) columns, ctypes.POINTER(ctypes.c_int) rows)
    addfunc(lib, "imaqImageToArray", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, Rect, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "rect", "columns", "rows"] )
    #  ctypes.c_int imaqImageToImage(ctypes.c_void_p largeImage, ctypes.c_void_p smallImage, ctypes.c_void_p dest, ctypes.POINTER(Rect) offset, ctypes.c_void_p mask, ctypes.c_int keepOverlays)
    addfunc(lib, "imaqImageToImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(Rect), ctypes.c_void_p, ctypes.c_int],
            argnames = ["largeImage", "smallImage", "dest", "offset", "mask", "keepOverlays"] )
    #  ctypes.c_int imaqChangeColorSpace2(ctypes.POINTER(ctypes.c_int) sourceColor, ctypes.c_int sourceSpace, ctypes.c_int destSpace, ctypes.c_double offset, ctypes.POINTER(CIEXYZValue) whiteReference)
    addfunc(lib, "imaqChangeColorSpace2", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(CIEXYZValue)],
            argnames = ["sourceColor", "sourceSpace", "destSpace", "offset", "whiteReference"] )
    #  ctypes.c_int imaqColorBCGTransform(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(BCGOptions) redOptions, ctypes.POINTER(BCGOptions) greenOptions, ctypes.POINTER(BCGOptions) blueOptions, ctypes.c_void_p mask)
    addfunc(lib, "imaqColorBCGTransform", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(BCGOptions), ctypes.POINTER(BCGOptions), ctypes.POINTER(BCGOptions), ctypes.c_void_p],
            argnames = ["dest", "source", "redOptions", "greenOptions", "blueOptions", "mask"] )
    #  ctypes.c_int imaqColorEqualize(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int colorEqualization)
    addfunc(lib, "imaqColorEqualize", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "colorEqualization"] )
    #  ctypes.POINTER(ColorHistogramReport) imaqColorHistogram3(ctypes.c_void_p image, ctypes.c_int numClasses, ctypes.c_int mode, ctypes.POINTER(CIEXYZValue) whiteReference, ctypes.POINTER(RangeFloat) range1, ctypes.POINTER(RangeFloat) range2, ctypes.POINTER(RangeFloat) range3, ctypes.c_void_p mask)
    addfunc(lib, "imaqColorHistogram3", restype = ctypes.POINTER(ColorHistogramReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(CIEXYZValue), ctypes.POINTER(RangeFloat), ctypes.POINTER(RangeFloat), ctypes.POINTER(RangeFloat), ctypes.c_void_p],
            argnames = ["image", "numClasses", "mode", "whiteReference", "range1", "range2", "range3", "mask"] )
    #  ctypes.c_int imaqColorLookup(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int mode, ctypes.c_void_p mask, ctypes.POINTER(ctypes.c_short) plane1, ctypes.POINTER(ctypes.c_short) plane2, ctypes.POINTER(ctypes.c_short) plane3)
    addfunc(lib, "imaqColorLookup", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_short), ctypes.POINTER(ctypes.c_short), ctypes.POINTER(ctypes.c_short)],
            argnames = ["dest", "source", "mode", "mask", "plane1", "plane2", "plane3"] )
    #  ctypes.c_int imaqColorThreshold(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int replaceValue, ctypes.c_int mode, ctypes.POINTER(Range) plane1Range, ctypes.POINTER(Range) plane2Range, ctypes.POINTER(Range) plane3Range)
    addfunc(lib, "imaqColorThreshold", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(Range), ctypes.POINTER(Range), ctypes.POINTER(Range)],
            argnames = ["dest", "source", "replaceValue", "mode", "plane1Range", "plane2Range", "plane3Range"] )
    #  ctypes.POINTER(SupervisedColorSegmentationReport) imaqSupervisedColorSegmentation(ctypes.c_void_p session, ctypes.c_void_p labelImage, ctypes.c_void_p srcImage, ctypes.c_void_p roi, ctypes.POINTER(ROILabel) labelIn, ctypes.c_uint numLabelIn, ctypes.c_int maxDistance, ctypes.c_int minIdentificationScore, ctypes.POINTER(ColorSegmenationOptions) segmentOptions)
    addfunc(lib, "imaqSupervisedColorSegmentation", restype = ctypes.POINTER(SupervisedColorSegmentationReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ROILabel), ctypes.c_uint, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ColorSegmenationOptions)],
            argnames = ["session", "labelImage", "srcImage", "roi", "labelIn", "numLabelIn", "maxDistance", "minIdentificationScore", "segmentOptions"] )
    #  ctypes.c_int imaqGetColorSegmentationMaxDistance(ctypes.c_void_p session, ctypes.POINTER(ColorSegmenationOptions) segmentOptions, ctypes.c_int distLevel, ctypes.POINTER(ctypes.c_int) maxDistance)
    addfunc(lib, "imaqGetColorSegmentationMaxDistance", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ColorSegmenationOptions), ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["session", "segmentOptions", "distLevel", "maxDistance"] )
    #  ctypes.c_int imaqBCGTransform(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(BCGOptions) options, ctypes.c_void_p mask)
    addfunc(lib, "imaqBCGTransform", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(BCGOptions), ctypes.c_void_p],
            argnames = ["dest", "source", "options", "mask"] )
    #  ctypes.c_int imaqEqualize(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_float min, ctypes.c_float max, ctypes.c_void_p mask)
    addfunc(lib, "imaqEqualize", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_void_p],
            argnames = ["dest", "source", "min", "max", "mask"] )
    #  ctypes.c_int imaqInverse(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_void_p mask)
    addfunc(lib, "imaqInverse", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source", "mask"] )
    #  ctypes.c_int imaqMathTransform(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int method, ctypes.c_float rangeMin, ctypes.c_float rangeMax, ctypes.c_float power, ctypes.c_void_p mask)
    addfunc(lib, "imaqMathTransform", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_float, ctypes.c_void_p],
            argnames = ["dest", "source", "method", "rangeMin", "rangeMax", "power", "mask"] )
    #  ctypes.c_int imaqWatershedTransform(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int connectivity8, ctypes.POINTER(ctypes.c_int) zoneCount)
    addfunc(lib, "imaqWatershedTransform", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "connectivity8", "zoneCount"] )
    #  ctypes.c_int imaqLookup2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ctypes.c_int) table, ctypes.c_void_p mask)
    addfunc(lib, "imaqLookup2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.c_void_p],
            argnames = ["dest", "source", "table", "mask"] )
    #  ctypes.c_int imaqAreScrollbarsVisible(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_int) visible)
    addfunc(lib, "imaqAreScrollbarsVisible", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["windowNumber", "visible"] )
    #  ctypes.c_int imaqBringWindowToTop(ctypes.c_int windowNumber)
    addfunc(lib, "imaqBringWindowToTop", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["windowNumber"] )
    #  ctypes.c_int imaqGetMousePos(ctypes.POINTER(Point) position, ctypes.POINTER(ctypes.c_int) windowNumber)
    addfunc(lib, "imaqGetMousePos", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(Point), ctypes.POINTER(ctypes.c_int)],
            argnames = ["position", "windowNumber"] )
    #  ctypes.POINTER(Palette) imaqGetPalette(ctypes.c_int paletteType)
    addfunc(lib, "imaqGetPalette", restype = ctypes.POINTER(Palette),
            argtypes = [ctypes.c_int],
            argnames = ["paletteType"] )
    #  ctypes.c_int imaqGetWindowBackground(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_int) fillStyle, ctypes.POINTER(ctypes.c_int) hatchStyle, ctypes.POINTER(RGBValue) fillColor, ctypes.POINTER(RGBValue) backgroundColor)
    addfunc(lib, "imaqGetWindowBackground", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(RGBValue), ctypes.POINTER(RGBValue)],
            argnames = ["windowNumber", "fillStyle", "hatchStyle", "fillColor", "backgroundColor"] )
    #  ctypes.c_int imaqGetWindowDisplayMapping(ctypes.c_int windowNum, ctypes.POINTER(DisplayMapping) mapping)
    addfunc(lib, "imaqGetWindowDisplayMapping", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(DisplayMapping)],
            argnames = ["windowNum", "mapping"] )
    #  ctypes.c_int imaqGetWindowGrid(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_int) xResolution, ctypes.POINTER(ctypes.c_int) yResolution)
    addfunc(lib, "imaqGetWindowGrid", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["windowNumber", "xResolution", "yResolution"] )
    #  ctypes.c_int imaqGetWindowHandle(ctypes.POINTER(ctypes.c_int) handle)
    addfunc(lib, "imaqGetWindowHandle", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["handle"] )
    #  ctypes.c_int imaqGetWindowPos(ctypes.c_int windowNumber, ctypes.POINTER(Point) position)
    addfunc(lib, "imaqGetWindowPos", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(Point)],
            argnames = ["windowNumber", "position"] )
    #  ctypes.c_int imaqGetWindowSize(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_int) width, ctypes.POINTER(ctypes.c_int) height)
    addfunc(lib, "imaqGetWindowSize", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["windowNumber", "width", "height"] )
    #  ctypes.c_char_p imaqGetWindowTitle(ctypes.c_int windowNumber)
    addfunc(lib, "imaqGetWindowTitle", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_int],
            argnames = ["windowNumber"] )
    #  ctypes.c_int imaqGetWindowZoom2(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_float) xZoom, ctypes.POINTER(ctypes.c_float) yZoom)
    addfunc(lib, "imaqGetWindowZoom2", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["windowNumber", "xZoom", "yZoom"] )
    #  ctypes.c_int imaqIsWindowNonTearing(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_int) nonTearing)
    addfunc(lib, "imaqIsWindowNonTearing", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["windowNumber", "nonTearing"] )
    #  ctypes.c_int imaqIsWindowVisible(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_int) visible)
    addfunc(lib, "imaqIsWindowVisible", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["windowNumber", "visible"] )
    #  ctypes.c_int imaqMoveWindow(ctypes.c_int windowNumber, Point position)
    addfunc(lib, "imaqMoveWindow", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, Point],
            argnames = ["windowNumber", "position"] )
    #  ctypes.c_int imaqSetupWindow(ctypes.c_int windowNumber, ctypes.c_int configuration)
    addfunc(lib, "imaqSetupWindow", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["windowNumber", "configuration"] )
    #  ctypes.c_int imaqSetWindowBackground(ctypes.c_int windowNumber, ctypes.c_int fillStyle, ctypes.c_int hatchStyle, ctypes.POINTER(RGBValue) fillColor, ctypes.POINTER(RGBValue) backgroundColor)
    addfunc(lib, "imaqSetWindowBackground", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.POINTER(RGBValue)],
            argnames = ["windowNumber", "fillStyle", "hatchStyle", "fillColor", "backgroundColor"] )
    #  ctypes.c_int imaqSetWindowDisplayMapping(ctypes.c_int windowNumber, ctypes.POINTER(DisplayMapping) mapping)
    addfunc(lib, "imaqSetWindowDisplayMapping", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(DisplayMapping)],
            argnames = ["windowNumber", "mapping"] )
    #  ctypes.c_int imaqSetWindowGrid(ctypes.c_int windowNumber, ctypes.c_int xResolution, ctypes.c_int yResolution)
    addfunc(lib, "imaqSetWindowGrid", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["windowNumber", "xResolution", "yResolution"] )
    #  ctypes.c_int imaqSetWindowMaxContourCount(ctypes.c_int windowNumber, ctypes.c_uint maxContourCount)
    addfunc(lib, "imaqSetWindowMaxContourCount", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_uint],
            argnames = ["windowNumber", "maxContourCount"] )
    #  ctypes.c_int imaqSetWindowNonTearing(ctypes.c_int windowNumber, ctypes.c_int nonTearing)
    addfunc(lib, "imaqSetWindowNonTearing", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["windowNumber", "nonTearing"] )
    #  ctypes.c_int imaqSetWindowPalette(ctypes.c_int windowNumber, ctypes.c_int type, ctypes.POINTER(RGBValue) palette, ctypes.c_int numColors)
    addfunc(lib, "imaqSetWindowPalette", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.c_int],
            argnames = ["windowNumber", "type", "palette", "numColors"] )
    #  ctypes.c_int imaqSetWindowSize(ctypes.c_int windowNumber, ctypes.c_int width, ctypes.c_int height)
    addfunc(lib, "imaqSetWindowSize", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["windowNumber", "width", "height"] )
    #  ctypes.c_int imaqSetWindowThreadPolicy(ctypes.c_int policy)
    addfunc(lib, "imaqSetWindowThreadPolicy", restype = ctypes.c_int,
            argtypes = [ctypes.c_int],
            argnames = ["policy"] )
    #  ctypes.c_int imaqSetWindowTitle(ctypes.c_int windowNumber, ctypes.c_char_p title)
    addfunc(lib, "imaqSetWindowTitle", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_char_p],
            argnames = ["windowNumber", "title"] )
    #  ctypes.c_int imaqSetWindowZoomToFit(ctypes.c_int windowNumber, ctypes.c_int zoomToFit)
    addfunc(lib, "imaqSetWindowZoomToFit", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["windowNumber", "zoomToFit"] )
    #  ctypes.c_int imaqShowScrollbars(ctypes.c_int windowNumber, ctypes.c_int visible)
    addfunc(lib, "imaqShowScrollbars", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["windowNumber", "visible"] )
    #  ctypes.c_int imaqZoomWindow2(ctypes.c_int windowNumber, ctypes.c_float xZoom, ctypes.c_float yZoom, Point center)
    addfunc(lib, "imaqZoomWindow2", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_float, ctypes.c_float, Point],
            argnames = ["windowNumber", "xZoom", "yZoom", "center"] )
    #  ctypes.POINTER(ctypes.c_float) imaqGetKernel(ctypes.c_int family, ctypes.c_int size, ctypes.c_int number)
    addfunc(lib, "imaqGetKernel", restype = ctypes.POINTER(ctypes.c_float),
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["family", "size", "number"] )
    #  Annulus imaqMakeAnnulus(Point center, ctypes.c_int innerRadius, ctypes.c_int outerRadius, ctypes.c_double startAngle, ctypes.c_double endAngle)
    addfunc(lib, "imaqMakeAnnulus", restype = Annulus,
            argtypes = [Point, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double],
            argnames = ["center", "innerRadius", "outerRadius", "startAngle", "endAngle"] )
    #  Point imaqMakePoint(ctypes.c_int xCoordinate, ctypes.c_int yCoordinate)
    addfunc(lib, "imaqMakePoint", restype = Point,
            argtypes = [ctypes.c_int, ctypes.c_int],
            argnames = ["xCoordinate", "yCoordinate"] )
    #  PointFloat imaqMakePointFloat(ctypes.c_float xCoordinate, ctypes.c_float yCoordinate)
    addfunc(lib, "imaqMakePointFloat", restype = PointFloat,
            argtypes = [ctypes.c_float, ctypes.c_float],
            argnames = ["xCoordinate", "yCoordinate"] )
    #  Rect imaqMakeRect(ctypes.c_int top, ctypes.c_int left, ctypes.c_int height, ctypes.c_int width)
    addfunc(lib, "imaqMakeRect", restype = Rect,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["top", "left", "height", "width"] )
    #  Rect imaqMakeRectFromRotatedRect(RotatedRect rotatedRect)
    addfunc(lib, "imaqMakeRectFromRotatedRect", restype = Rect,
            argtypes = [RotatedRect],
            argnames = ["rotatedRect"] )
    #  RotatedRect imaqMakeRotatedRect(ctypes.c_int top, ctypes.c_int left, ctypes.c_int height, ctypes.c_int width, ctypes.c_double angle)
    addfunc(lib, "imaqMakeRotatedRect", restype = RotatedRect,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_double],
            argnames = ["top", "left", "height", "width", "angle"] )
    #  RotatedRect imaqMakeRotatedRectFromRect(Rect rect)
    addfunc(lib, "imaqMakeRotatedRectFromRect", restype = RotatedRect,
            argtypes = [Rect],
            argnames = ["rect"] )
    #  ctypes.c_int imaqMulticoreOptions(ctypes.c_int operation, ctypes.POINTER(ctypes.c_uint) customNumCores)
    addfunc(lib, "imaqMulticoreOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["operation", "customNumCores"] )
    #  ctypes.POINTER(ctypes.c_char_p) imaqEnumerateCustomKeys(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_uint) size)
    addfunc(lib, "imaqEnumerateCustomKeys", restype = ctypes.POINTER(ctypes.c_char_p),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "size"] )
    #  ctypes.c_int imaqGetBitDepth(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_uint) bitDepth)
    addfunc(lib, "imaqGetBitDepth", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "bitDepth"] )
    #  ctypes.c_int imaqGetBytesPerPixel(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_int) byteCount)
    addfunc(lib, "imaqGetBytesPerPixel", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "byteCount"] )
    #  ctypes.c_int imaqGetImageInfo(ctypes.c_void_p image, ctypes.POINTER(ImageInfo) info)
    addfunc(lib, "imaqGetImageInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ImageInfo)],
            argnames = ["image", "info"] )
    #  ctypes.c_int imaqGetImageSize(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_int) width, ctypes.POINTER(ctypes.c_int) height)
    addfunc(lib, "imaqGetImageSize", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "width", "height"] )
    #  ctypes.c_int imaqGetImageType(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_int) type)
    addfunc(lib, "imaqGetImageType", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "type"] )
    #  ctypes.c_int imaqGetMaskOffset(ctypes.c_void_p image, ctypes.POINTER(Point) offset)
    addfunc(lib, "imaqGetMaskOffset", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point)],
            argnames = ["image", "offset"] )
    #  ctypes.c_void_p imaqGetPixelAddress(ctypes.c_void_p image, Point pixel)
    addfunc(lib, "imaqGetPixelAddress", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, Point],
            argnames = ["image", "pixel"] )
    #  ctypes.c_int imaqGetVisionInfoTypes(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_uint) present)
    addfunc(lib, "imaqGetVisionInfoTypes", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "present"] )
    #  ctypes.c_int imaqIsImageEmpty(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_int) empty)
    addfunc(lib, "imaqIsImageEmpty", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "empty"] )
    #  ctypes.c_void_p imaqReadCustomData(ctypes.c_void_p image, ctypes.c_char_p key, ctypes.POINTER(ctypes.c_uint) size)
    addfunc(lib, "imaqReadCustomData", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "key", "size"] )
    #  ctypes.c_int imaqRemoveCustomData(ctypes.c_void_p image, ctypes.c_char_p key)
    addfunc(lib, "imaqRemoveCustomData", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["image", "key"] )
    #  ctypes.c_int imaqRemoveVisionInfo2(ctypes.c_void_p image, ctypes.c_uint info)
    addfunc(lib, "imaqRemoveVisionInfo2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["image", "info"] )
    #  ctypes.c_int imaqSetBitDepth(ctypes.c_void_p image, ctypes.c_uint bitDepth)
    addfunc(lib, "imaqSetBitDepth", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["image", "bitDepth"] )
    #  ctypes.c_int imaqSetImageSize(ctypes.c_void_p image, ctypes.c_int width, ctypes.c_int height)
    addfunc(lib, "imaqSetImageSize", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["image", "width", "height"] )
    #  ctypes.c_int imaqSetMaskOffset(ctypes.c_void_p image, Point offset)
    addfunc(lib, "imaqSetMaskOffset", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point],
            argnames = ["image", "offset"] )
    #  ctypes.c_int imaqWriteCustomData(ctypes.c_void_p image, ctypes.c_char_p key, ctypes.c_void_p data, ctypes.c_uint size)
    addfunc(lib, "imaqWriteCustomData", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.c_uint],
            argnames = ["image", "key", "data", "size"] )
    #  ctypes.c_int imaqCopyVisionInfo(ctypes.c_void_p source, ctypes.c_void_p dest, ctypes.POINTER(ctypes.c_uint) infoFlags)
    addfunc(lib, "imaqCopyVisionInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["source", "dest", "infoFlags"] )
    #  ctypes.POINTER(ColorInformation) imaqLearnColor(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int sensitivity, ctypes.c_int saturation)
    addfunc(lib, "imaqLearnColor", restype = ctypes.POINTER(ColorInformation),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["image", "roi", "sensitivity", "saturation"] )
    #  ctypes.POINTER(ctypes.c_int) imaqMatchColor(ctypes.c_void_p image, ctypes.POINTER(ColorInformation) info, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numScores)
    addfunc(lib, "imaqMatchColor", restype = ctypes.POINTER(ctypes.c_int),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ColorInformation), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "info", "roi", "numScores"] )
    #  ctypes.c_int imaqArrayToComplexPlane(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ctypes.c_float) newPixels, ctypes.c_int plane)
    addfunc(lib, "imaqArrayToComplexPlane", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_int],
            argnames = ["dest", "source", "newPixels", "plane"] )
    #  ctypes.POINTER(ctypes.c_float) imaqComplexPlaneToArray(ctypes.c_void_p image, ctypes.c_int plane, Rect rect, ctypes.POINTER(ctypes.c_int) rows, ctypes.POINTER(ctypes.c_int) columns)
    addfunc(lib, "imaqComplexPlaneToArray", restype = ctypes.POINTER(ctypes.c_float),
            argtypes = [ctypes.c_void_p, ctypes.c_int, Rect, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "plane", "rect", "rows", "columns"] )
    #  ctypes.c_int imaqExtractColorPlanes(ctypes.c_void_p image, ctypes.c_int mode, ctypes.c_void_p plane1, ctypes.c_void_p plane2, ctypes.c_void_p plane3)
    addfunc(lib, "imaqExtractColorPlanes", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["image", "mode", "plane1", "plane2", "plane3"] )
    #  ctypes.c_int imaqExtractComplexPlane(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int plane)
    addfunc(lib, "imaqExtractComplexPlane", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "plane"] )
    #  ctypes.c_int imaqFillImage(ctypes.c_void_p image, ctypes.c_int value, ctypes.c_void_p mask)
    addfunc(lib, "imaqFillImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p],
            argnames = ["image", "value", "mask"] )
    #  ctypes.c_void_p imaqGetLine(ctypes.c_void_p image, Point start, Point end, ctypes.POINTER(ctypes.c_int) numPoints)
    addfunc(lib, "imaqGetLine", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, Point, Point, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "start", "end", "numPoints"] )
    #  ctypes.c_int imaqGetPixel(ctypes.c_void_p image, Point pixel, ctypes.POINTER(ctypes.c_int) value)
    addfunc(lib, "imaqGetPixel", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pixel", "value"] )
    #  ctypes.c_int imaqReplaceColorPlanes(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int mode, ctypes.c_void_p plane1, ctypes.c_void_p plane2, ctypes.c_void_p plane3)
    addfunc(lib, "imaqReplaceColorPlanes", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source", "mode", "plane1", "plane2", "plane3"] )
    #  ctypes.c_int imaqReplaceComplexPlane(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_void_p newValues, ctypes.c_int plane)
    addfunc(lib, "imaqReplaceComplexPlane", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "newValues", "plane"] )
    #  ctypes.c_int imaqSetLine(ctypes.c_void_p image, ctypes.c_void_p array, ctypes.c_int arraySize, Point start, Point end)
    addfunc(lib, "imaqSetLine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, Point, Point],
            argnames = ["image", "array", "arraySize", "start", "end"] )
    #  ctypes.c_int imaqSetPixel(ctypes.c_void_p image, Point coord, ctypes.c_int value)
    addfunc(lib, "imaqSetPixel", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, ctypes.c_int],
            argnames = ["image", "coord", "value"] )
    #  ctypes.c_int imaqClearOverlay(ctypes.c_void_p image, ctypes.c_char_p group)
    addfunc(lib, "imaqClearOverlay", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["image", "group"] )
    #  ctypes.c_int imaqCopyOverlay(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_char_p group)
    addfunc(lib, "imaqCopyOverlay", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["dest", "source", "group"] )
    #  ctypes.c_int imaqGetOverlayProperties(ctypes.c_void_p image, ctypes.c_char_p group, ctypes.POINTER(TransformBehaviors) transformBehaviors)
    addfunc(lib, "imaqGetOverlayProperties", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(TransformBehaviors)],
            argnames = ["image", "group", "transformBehaviors"] )
    #  ctypes.c_int imaqMergeOverlay(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(RGBValue) palette, ctypes.c_uint numColors, ctypes.c_char_p group)
    addfunc(lib, "imaqMergeOverlay", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(RGBValue), ctypes.c_uint, ctypes.c_char_p],
            argnames = ["dest", "source", "palette", "numColors", "group"] )
    #  ctypes.c_int imaqOverlayArc(ctypes.c_void_p image, ctypes.POINTER(ArcInfo) arc, ctypes.POINTER(RGBValue) color, ctypes.c_int drawMode, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayArc", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ArcInfo), ctypes.POINTER(RGBValue), ctypes.c_int, ctypes.c_char_p],
            argnames = ["image", "arc", "color", "drawMode", "group"] )
    #  ctypes.c_int imaqOverlayBitmap(ctypes.c_void_p image, Point destLoc, ctypes.POINTER(RGBValue) bitmap, ctypes.c_uint numCols, ctypes.c_uint numRows, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayBitmap", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, ctypes.POINTER(RGBValue), ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p],
            argnames = ["image", "destLoc", "bitmap", "numCols", "numRows", "group"] )
    #  ctypes.c_int imaqOverlayClosedContour(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.POINTER(RGBValue) color, ctypes.c_int drawMode, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayClosedContour", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.c_int, ctypes.c_char_p],
            argnames = ["image", "points", "numPoints", "color", "drawMode", "group"] )
    #  ctypes.c_int imaqOverlayLine(ctypes.c_void_p image, Point start, Point end, ctypes.POINTER(RGBValue) color, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayLine", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, Point, ctypes.POINTER(RGBValue), ctypes.c_char_p],
            argnames = ["image", "start", "end", "color", "group"] )
    #  ctypes.c_int imaqOverlayMetafile(ctypes.c_void_p image, ctypes.c_void_p metafile, Rect rect, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayMetafile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, Rect, ctypes.c_char_p],
            argnames = ["image", "metafile", "rect", "group"] )
    #  ctypes.c_int imaqOverlayOpenContour(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.POINTER(RGBValue) color, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayOpenContour", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.c_char_p],
            argnames = ["image", "points", "numPoints", "color", "group"] )
    #  ctypes.c_int imaqOverlayOval(ctypes.c_void_p image, Rect boundingBox, ctypes.POINTER(RGBValue) color, ctypes.c_int drawMode, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayOval", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Rect, ctypes.POINTER(RGBValue), ctypes.c_int, ctypes.c_char_p],
            argnames = ["image", "boundingBox", "color", "drawMode", "group"] )
    #  ctypes.c_int imaqOverlayPoints(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.POINTER(RGBValue) colors, ctypes.c_int numColors, ctypes.c_int symbol, ctypes.POINTER(UserPointSymbol) userSymbol, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayPoints", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.c_int, ctypes.c_int, ctypes.POINTER(UserPointSymbol), ctypes.c_char_p],
            argnames = ["image", "points", "numPoints", "colors", "numColors", "symbol", "userSymbol", "group"] )
    #  ctypes.c_int imaqOverlayRect(ctypes.c_void_p image, Rect rect, ctypes.POINTER(RGBValue) color, ctypes.c_int drawMode, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayRect", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Rect, ctypes.POINTER(RGBValue), ctypes.c_int, ctypes.c_char_p],
            argnames = ["image", "rect", "color", "drawMode", "group"] )
    #  ctypes.c_int imaqOverlayROI(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int symbol, ctypes.POINTER(UserPointSymbol) userSymbol, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayROI", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(UserPointSymbol), ctypes.c_char_p],
            argnames = ["image", "roi", "symbol", "userSymbol", "group"] )
    #  ctypes.c_int imaqOverlayLines3(ctypes.c_void_p image, ctypes.POINTER(PointDouble) points, ctypes.c_int numPoints, ctypes.c_int drawMode, ctypes.POINTER(RGBValue) color, ctypes.c_char_p group, ctypes.c_uint useDcWidth, ctypes.c_uint width)
    addfunc(lib, "imaqOverlayLines3", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(PointDouble), ctypes.c_int, ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.c_char_p, ctypes.c_uint, ctypes.c_uint],
            argnames = ["image", "points", "numPoints", "drawMode", "color", "group", "useDcWidth", "width"] )
    #  ctypes.c_int imaqOverlayText(ctypes.c_void_p image, Point origin, ctypes.c_char_p text, ctypes.POINTER(RGBValue) color, ctypes.POINTER(OverlayTextOptions) options, ctypes.c_char_p group)
    addfunc(lib, "imaqOverlayText", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, ctypes.c_char_p, ctypes.POINTER(RGBValue), ctypes.POINTER(OverlayTextOptions), ctypes.c_char_p],
            argnames = ["image", "origin", "text", "color", "options", "group"] )
    #  ctypes.c_int imaqSetOverlayColor(ctypes.c_void_p image, ctypes.POINTER(OverlayGroupColor) groupColors, ctypes.c_int numEntries)
    addfunc(lib, "imaqSetOverlayColor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(OverlayGroupColor), ctypes.c_int],
            argnames = ["image", "groupColors", "numEntries"] )
    #  ctypes.c_int imaqSetOverlayProperties(ctypes.c_void_p image, ctypes.c_char_p group, ctypes.POINTER(TransformBehaviors) transformBehaviors)
    addfunc(lib, "imaqSetOverlayProperties", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(TransformBehaviors)],
            argnames = ["image", "group", "transformBehaviors"] )
    #  ctypes.c_int imaqOverlayMotionVectors(ctypes.c_void_p srcImage, ctypes.c_void_p velX, ctypes.c_void_p velY, ctypes.c_int velocityRep, ctypes.c_double threshold, ctypes.c_double scale, ctypes.c_int stepSize, ctypes.POINTER(RGBValue) color, ctypes.c_char_p groupName)
    addfunc(lib, "imaqOverlayMotionVectors", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.POINTER(RGBValue), ctypes.c_char_p],
            argnames = ["srcImage", "velX", "velY", "velocityRep", "threshold", "scale", "stepSize", "color", "groupName"] )
    #  ctypes.POINTER(MeterArc) imaqGetMeterArc(ctypes.c_int lightNeedle, ctypes.c_int mode, ctypes.c_void_p roi, PointFloat base, PointFloat start, PointFloat end)
    addfunc(lib, "imaqGetMeterArc", restype = ctypes.POINTER(MeterArc),
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, PointFloat, PointFloat, PointFloat],
            argnames = ["lightNeedle", "mode", "roi", "base", "start", "end"] )
    #  ctypes.c_int imaqReadMeter(ctypes.c_void_p image, ctypes.POINTER(MeterArc) arcInfo, ctypes.POINTER(ctypes.c_double) percentage, ctypes.POINTER(PointFloat) endOfNeedle)
    addfunc(lib, "imaqReadMeter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(MeterArc), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(PointFloat)],
            argnames = ["image", "arcInfo", "percentage", "endOfNeedle"] )
    #  ctypes.POINTER(BarcodeInfo) imaqReadBarcode(ctypes.c_void_p image, ctypes.c_int type, ctypes.c_void_p roi, ctypes.c_int validate)
    addfunc(lib, "imaqReadBarcode", restype = ctypes.POINTER(BarcodeInfo),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int],
            argnames = ["image", "type", "roi", "validate"] )
    #  ctypes.POINTER(BarcodeInfoReport) imaqReadBarcode2(ctypes.c_void_p image, ctypes.POINTER(Barcode1DSearchOptions) searchOptions, ctypes.POINTER(ctypes.c_int) barcodeTypes, ctypes.c_uint numOfTypes, ctypes.c_uint numRequiredBarcodes, ctypes.c_void_p roi, ctypes.c_int validate)
    addfunc(lib, "imaqReadBarcode2", restype = ctypes.POINTER(BarcodeInfoReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Barcode1DSearchOptions), ctypes.POINTER(ctypes.c_int), ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_int],
            argnames = ["image", "searchOptions", "barcodeTypes", "numOfTypes", "numRequiredBarcodes", "roi", "validate"] )
    #  ctypes.POINTER(BarcodeInfoReportandGrading) imaqReadBarcode3(ctypes.c_void_p image, ctypes.POINTER(Barcode1DSearchOptions) searchOptions, ctypes.POINTER(ctypes.c_int) barcodeTypes, ctypes.c_uint numOfTypes, ctypes.c_uint numRequiredBarcodes, ctypes.c_void_p roi, ctypes.c_int validate, ctypes.POINTER(BarcodeGradingOptions) gradingOptions)
    addfunc(lib, "imaqReadBarcode3", restype = ctypes.POINTER(BarcodeInfoReportandGrading),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Barcode1DSearchOptions), ctypes.POINTER(ctypes.c_int), ctypes.c_uint, ctypes.c_uint, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(BarcodeGradingOptions)],
            argnames = ["image", "searchOptions", "barcodeTypes", "numOfTypes", "numRequiredBarcodes", "roi", "validate", "gradingOptions"] )
    #  ctypes.POINTER(DataMatrixReport) imaqReadDataMatrixBarcode2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int prepareForGrading, ctypes.POINTER(DataMatrixDescriptionOptions) descriptionOptions, ctypes.POINTER(DataMatrixSizeOptions) sizeOptions, ctypes.POINTER(DataMatrixSearchOptions) searchOptions)
    addfunc(lib, "imaqReadDataMatrixBarcode2", restype = ctypes.POINTER(DataMatrixReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(DataMatrixDescriptionOptions), ctypes.POINTER(DataMatrixSizeOptions), ctypes.POINTER(DataMatrixSearchOptions)],
            argnames = ["image", "roi", "prepareForGrading", "descriptionOptions", "sizeOptions", "searchOptions"] )
    #  ctypes.POINTER(DataMatrixReport) imaqReadDataMatrixBarcode3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int prepareForGrading, ctypes.POINTER(DataMatrixDescriptionOptions) descriptionOptions, ctypes.POINTER(DataMatrixSizeOptions) sizeOptions, ctypes.POINTER(DataMatrixSearchOptions) searchOptions, ctypes.POINTER(AdvancedDataMatrixOptions) barcodeAdvancedOptions, ctypes.c_uint numAdvancedOptions)
    addfunc(lib, "imaqReadDataMatrixBarcode3", restype = ctypes.POINTER(DataMatrixReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(DataMatrixDescriptionOptions), ctypes.POINTER(DataMatrixSizeOptions), ctypes.POINTER(DataMatrixSearchOptions), ctypes.POINTER(AdvancedDataMatrixOptions), ctypes.c_uint],
            argnames = ["image", "roi", "prepareForGrading", "descriptionOptions", "sizeOptions", "searchOptions", "barcodeAdvancedOptions", "numAdvancedOptions"] )
    #  ctypes.POINTER(DataMatrixReport) imaqReadDataMatrixBarcode4(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int prepareForGrading, ctypes.POINTER(DataMatrixDescriptionOptions) descriptionOptions, ctypes.POINTER(DataMatrixSizeOptions) sizeOptions, ctypes.POINTER(DataMatrixSearchOptions) searchOptions, ctypes.POINTER(AdvancedDataMatrixOptions) barcodeAdvancedOptions, ctypes.c_uint numAdvancedOptions, ctypes.POINTER(ctypes.c_float) meanLight)
    addfunc(lib, "imaqReadDataMatrixBarcode4", restype = ctypes.POINTER(DataMatrixReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(DataMatrixDescriptionOptions), ctypes.POINTER(DataMatrixSizeOptions), ctypes.POINTER(DataMatrixSearchOptions), ctypes.POINTER(AdvancedDataMatrixOptions), ctypes.c_uint, ctypes.POINTER(ctypes.c_float)],
            argnames = ["image", "roi", "prepareForGrading", "descriptionOptions", "sizeOptions", "searchOptions", "barcodeAdvancedOptions", "numAdvancedOptions", "meanLight"] )
    #  ctypes.POINTER(Barcode2DInfo) imaqReadPDF417Barcode(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int searchMode, ctypes.POINTER(ctypes.c_uint) numBarcodes)
    addfunc(lib, "imaqReadPDF417Barcode", restype = ctypes.POINTER(Barcode2DInfo),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "roi", "searchMode", "numBarcodes"] )
    #  ctypes.POINTER(QRCodeReport) imaqReadQRCode(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int reserved, ctypes.POINTER(QRCodeDescriptionOptions) descriptionOptions, ctypes.POINTER(QRCodeSizeOptions) sizeOptions, ctypes.POINTER(QRCodeSearchOptions) searchOptions)
    addfunc(lib, "imaqReadQRCode", restype = ctypes.POINTER(QRCodeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(QRCodeDescriptionOptions), ctypes.POINTER(QRCodeSizeOptions), ctypes.POINTER(QRCodeSearchOptions)],
            argnames = ["image", "roi", "reserved", "descriptionOptions", "sizeOptions", "searchOptions"] )
    #  ctypes.c_int imaqGradeDataMatrixBarcodeAIM(ctypes.c_void_p image, ctypes.POINTER(AIMGradeReport) report)
    addfunc(lib, "imaqGradeDataMatrixBarcodeAIM", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(AIMGradeReport)],
            argnames = ["image", "report"] )
    #  ctypes.c_int imaqGradeDataMatrixBarcodeAIMDPM(ctypes.c_void_p image, ctypes.POINTER(CalibReflectanceStruct) calibReflectance, ctypes.POINTER(AIMDPMGradeReport) report)
    addfunc(lib, "imaqGradeDataMatrixBarcodeAIMDPM", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CalibReflectanceStruct), ctypes.POINTER(AIMDPMGradeReport)],
            argnames = ["image", "calibReflectance", "report"] )
    #  ctypes.c_int imaqGradeDataMatrixBarcodeISO15415(ctypes.c_void_p image, ctypes.POINTER(GradeReportISO15415) report)
    addfunc(lib, "imaqGradeDataMatrixBarcodeISO15415", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(GradeReportISO15415)],
            argnames = ["image", "report"] )
    #  ctypes.c_int imaqGradeDataMatrixBarcodeISO16022(ctypes.c_void_p image, ctypes.POINTER(GradeReportISO16022) report)
    addfunc(lib, "imaqGradeDataMatrixBarcodeISO16022", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(GradeReportISO16022)],
            argnames = ["image", "report"] )
    #  ctypes.c_int imaqFindLCDSegments(ctypes.c_void_p roi, ctypes.c_void_p image, ctypes.POINTER(LCDOptions) options)
    addfunc(lib, "imaqFindLCDSegments", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(LCDOptions)],
            argnames = ["roi", "image", "options"] )
    #  ctypes.POINTER(LCDReport) imaqReadLCD(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(LCDOptions) options)
    addfunc(lib, "imaqReadLCD", restype = ctypes.POINTER(LCDReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(LCDOptions)],
            argnames = ["image", "roi", "options"] )
    #  ctypes.POINTER(ShapeReport2) imaqMatchShape2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_void_p templateImage, ctypes.c_int scaleInvariant, ctypes.c_int connectivity8, ctypes.c_double tolerance, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchShape2", restype = ctypes.POINTER(ShapeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "templateImage", "scaleInvariant", "connectivity8", "tolerance", "numMatches"] )
    #  ContourID imaqAddAnnulusContour(ctypes.c_void_p roi, Annulus annulus)
    addfunc(lib, "imaqAddAnnulusContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, Annulus],
            argnames = ["roi", "annulus"] )
    #  ContourID imaqAddClosedContour(ctypes.c_void_p roi, ctypes.POINTER(Point) points, ctypes.c_int numPoints)
    addfunc(lib, "imaqAddClosedContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int],
            argnames = ["roi", "points", "numPoints"] )
    #  ContourID imaqAddLineContour(ctypes.c_void_p roi, Point start, Point end)
    addfunc(lib, "imaqAddLineContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, Point, Point],
            argnames = ["roi", "start", "end"] )
    #  ContourID imaqAddOpenContour(ctypes.c_void_p roi, ctypes.POINTER(Point) points, ctypes.c_int numPoints)
    addfunc(lib, "imaqAddOpenContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int],
            argnames = ["roi", "points", "numPoints"] )
    #  ContourID imaqAddOvalContour(ctypes.c_void_p roi, Rect boundingBox)
    addfunc(lib, "imaqAddOvalContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, Rect],
            argnames = ["roi", "boundingBox"] )
    #  ContourID imaqAddPointContour(ctypes.c_void_p roi, Point point)
    addfunc(lib, "imaqAddPointContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, Point],
            argnames = ["roi", "point"] )
    #  ContourID imaqAddRectContour(ctypes.c_void_p roi, Rect rect)
    addfunc(lib, "imaqAddRectContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, Rect],
            argnames = ["roi", "rect"] )
    #  ContourID imaqAddRotatedRectContour2(ctypes.c_void_p roi, RotatedRect rect)
    addfunc(lib, "imaqAddRotatedRectContour2", restype = ContourID,
            argtypes = [ctypes.c_void_p, RotatedRect],
            argnames = ["roi", "rect"] )
    #  ctypes.c_int imaqContourLearn(ctypes.c_void_p image, ctypes.POINTER(LearnContourSetupData) setupData, ctypes.c_void_p mask)
    addfunc(lib, "imaqContourLearn", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(LearnContourSetupData), ctypes.c_void_p],
            argnames = ["image", "setupData", "mask"] )
    #  ctypes.POINTER(LearnContourSetupData) imaqContourSetupLearnPattern(ctypes.c_void_p image, ctypes.POINTER(GeometricAdvancedSetupDataOption) geometricOptions, ctypes.c_uint numGeometricOptions)
    addfunc(lib, "imaqContourSetupLearnPattern", restype = ctypes.POINTER(LearnContourSetupData),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(GeometricAdvancedSetupDataOption), ctypes.c_uint],
            argnames = ["image", "geometricOptions", "numGeometricOptions"] )
    #  ContourID imaqCopyContour(ctypes.c_void_p destRoi, ctypes.c_void_p sourceRoi, ContourID id)
    addfunc(lib, "imaqCopyContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ContourID],
            argnames = ["destRoi", "sourceRoi", "id"] )
    #  ContourID imaqGetContour(ctypes.c_void_p roi, ctypes.c_uint index)
    addfunc(lib, "imaqGetContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["roi", "index"] )
    #  ctypes.c_int imaqGetContourColor(ctypes.c_void_p roi, ContourID id, ctypes.POINTER(RGBValue) contourColor)
    addfunc(lib, "imaqGetContourColor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ContourID, ctypes.POINTER(RGBValue)],
            argnames = ["roi", "id", "contourColor"] )
    #  ctypes.c_int imaqGetContourCount(ctypes.c_void_p roi)
    addfunc(lib, "imaqGetContourCount", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["roi"] )
    #  ctypes.POINTER(ContourInfo2) imaqGetContourInfo2(ctypes.c_void_p roi, ContourID id)
    addfunc(lib, "imaqGetContourInfo2", restype = ctypes.POINTER(ContourInfo2),
            argtypes = [ctypes.c_void_p, ContourID],
            argnames = ["roi", "id"] )
    #  ctypes.c_int imaqMoveContour(ctypes.c_void_p roi, ContourID id, ctypes.c_int deltaX, ctypes.c_int deltaY)
    addfunc(lib, "imaqMoveContour", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ContourID, ctypes.c_int, ctypes.c_int],
            argnames = ["roi", "id", "deltaX", "deltaY"] )
    #  ctypes.c_int imaqRemoveContour(ctypes.c_void_p roi, ContourID id)
    addfunc(lib, "imaqRemoveContour", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ContourID],
            argnames = ["roi", "id"] )
    #  ctypes.c_int imaqSetContourColor(ctypes.c_void_p roi, ContourID id, ctypes.POINTER(RGBValue) color)
    addfunc(lib, "imaqSetContourColor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ContourID, ctypes.POINTER(RGBValue)],
            argnames = ["roi", "id", "color"] )
    #  ctypes.c_int imaqConstructROI2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int initialTool, ctypes.POINTER(ToolWindowOptions) tools, ctypes.POINTER(ConstructROIOptions2) options, ctypes.POINTER(ctypes.c_int) okay)
    addfunc(lib, "imaqConstructROI2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ToolWindowOptions), ctypes.POINTER(ConstructROIOptions2), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "roi", "initialTool", "tools", "options", "okay"] )
    #  ctypes.c_void_p imaqCreateROI()
    addfunc(lib, "imaqCreateROI", restype = ctypes.c_void_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int imaqGetROIBoundingBox(ctypes.c_void_p roi, ctypes.POINTER(Rect) boundingBox)
    addfunc(lib, "imaqGetROIBoundingBox", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Rect)],
            argnames = ["roi", "boundingBox"] )
    #  ctypes.c_int imaqGetROIColor(ctypes.c_void_p roi, ctypes.POINTER(RGBValue) roiColor)
    addfunc(lib, "imaqGetROIColor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(RGBValue)],
            argnames = ["roi", "roiColor"] )
    #  ctypes.c_void_p imaqGetWindowROI(ctypes.c_int windowNumber)
    addfunc(lib, "imaqGetWindowROI", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_int],
            argnames = ["windowNumber"] )
    #  ctypes.c_int imaqSetROIColor(ctypes.c_void_p roi, ctypes.POINTER(RGBValue) color)
    addfunc(lib, "imaqSetROIColor", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(RGBValue)],
            argnames = ["roi", "color"] )
    #  ctypes.c_int imaqSetWindowROI(ctypes.c_int windowNumber, ctypes.c_void_p roi)
    addfunc(lib, "imaqSetWindowROI", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_void_p],
            argnames = ["windowNumber", "roi"] )
    #  ctypes.POINTER(BlockStatisticsReport) imaqBlockStatistics(ctypes.c_void_p image, BlockSize blockSize, ctypes.c_int calculateMinMax)
    addfunc(lib, "imaqBlockStatistics", restype = ctypes.POINTER(BlockStatisticsReport),
            argtypes = [ctypes.c_void_p, BlockSize, ctypes.c_int],
            argnames = ["image", "blockSize", "calculateMinMax"] )
    #  ctypes.c_int imaqCentroid(ctypes.c_void_p image, ctypes.POINTER(PointFloat) centroid, ctypes.c_void_p mask)
    addfunc(lib, "imaqCentroid", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(PointFloat), ctypes.c_void_p],
            argnames = ["image", "centroid", "mask"] )
    #  ctypes.POINTER(Curve) imaqExtractCurves(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(ctypes.c_uint) numCurves)
    addfunc(lib, "imaqExtractCurves", restype = ctypes.POINTER(Curve),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CurveOptions), ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "roi", "curveOptions", "numCurves"] )
    #  ctypes.c_int imaqFastSSIM(ctypes.c_void_p testImage, ctypes.c_void_p referenceImage, ctypes.c_void_p ssimMap, ctypes.c_int windowSize, ctypes.POINTER(ctypes.c_double) meanSSIM, ctypes.POINTER(SSIMComponents) ssimComponents)
    addfunc(lib, "imaqFastSSIM", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(SSIMComponents)],
            argnames = ["testImage", "referenceImage", "ssimMap", "windowSize", "meanSSIM", "ssimComponents"] )
    #  ctypes.POINTER(HighLevelParticleAnalysisReport) imaqHighLevelParticleAnalysis(ctypes.c_void_p image, ctypes.c_int connectivity48)
    addfunc(lib, "imaqHighLevelParticleAnalysis", restype = ctypes.POINTER(HighLevelParticleAnalysisReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["image", "connectivity48"] )
    #  ctypes.POINTER(HistogramReport) imaqHistogram(ctypes.c_void_p image, ctypes.c_int numClasses, ctypes.c_float min, ctypes.c_float max, ctypes.c_void_p mask)
    addfunc(lib, "imaqHistogram", restype = ctypes.POINTER(HistogramReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_float, ctypes.c_void_p],
            argnames = ["image", "numClasses", "min", "max", "mask"] )
    #  ctypes.POINTER(LinearAverages) imaqLinearAverages2(ctypes.c_void_p image, ctypes.c_int mode, Rect rect)
    addfunc(lib, "imaqLinearAverages2", restype = ctypes.POINTER(LinearAverages),
            argtypes = [ctypes.c_void_p, ctypes.c_int, Rect],
            argnames = ["image", "mode", "rect"] )
    #  ctypes.POINTER(LineProfile) imaqLineProfile(ctypes.c_void_p image, Point start, Point end)
    addfunc(lib, "imaqLineProfile", restype = ctypes.POINTER(LineProfile),
            argtypes = [ctypes.c_void_p, Point, Point],
            argnames = ["image", "start", "end"] )
    #  ctypes.c_int imaqNormalSSIM(ctypes.c_void_p testImage, ctypes.c_void_p referenceImage, ctypes.c_void_p ssimMap, ctypes.c_int windowSize, ctypes.POINTER(ctypes.c_double) meanSSIM, ctypes.POINTER(SSIMComponents) ssimComponents)
    addfunc(lib, "imaqNormalSSIM", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(SSIMComponents)],
            argnames = ["testImage", "referenceImage", "ssimMap", "windowSize", "meanSSIM", "ssimComponents"] )
    #  ctypes.POINTER(QuantifyReport2) imaqQuantify2(ctypes.c_void_p image, ctypes.c_void_p mask)
    addfunc(lib, "imaqQuantify2", restype = ctypes.POINTER(QuantifyReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["image", "mask"] )
    #  ctypes.c_int imaqClearError()
    addfunc(lib, "imaqClearError", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_char_p imaqGetErrorText(ctypes.c_int errorCode)
    addfunc(lib, "imaqGetErrorText", restype = ctypes.c_char_p,
            argtypes = [ctypes.c_int],
            argnames = ["errorCode"] )
    #  ctypes.c_int imaqGetLastError()
    addfunc(lib, "imaqGetLastError", restype = ctypes.c_int,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_char_p imaqGetLastErrorFunc()
    addfunc(lib, "imaqGetLastErrorFunc", restype = ctypes.c_char_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int imaqSetError(ctypes.c_int errorCode, ctypes.c_char_p function)
    addfunc(lib, "imaqSetError", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_char_p],
            argnames = ["errorCode", "function"] )
    #  ctypes.POINTER(ThresholdData) imaqAutoThreshold3(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int numClasses, ctypes.c_int method, ctypes.c_int lookForParticleType, ctypes.c_float value, ctypes.POINTER(RangeFloat) limits, ctypes.c_void_p roi, ctypes.c_void_p mask)
    addfunc(lib, "imaqAutoThreshold3", restype = ctypes.POINTER(ThresholdData),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.POINTER(RangeFloat), ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source", "numClasses", "method", "lookForParticleType", "value", "limits", "roi", "mask"] )
    #  ctypes.c_int imaqLocalThreshold2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_uint windowWidth, ctypes.c_uint windowHeight, ctypes.c_int method, ctypes.c_double deviationWeight, ctypes.c_double sauvolaDeviationRange, ctypes.c_int type, ctypes.c_float replaceValue)
    addfunc(lib, "imaqLocalThreshold2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_int, ctypes.c_float],
            argnames = ["dest", "source", "windowWidth", "windowHeight", "method", "deviationWeight", "sauvolaDeviationRange", "type", "replaceValue"] )
    #  ctypes.c_int imaqMagicWand(ctypes.c_void_p dest, ctypes.c_void_p source, Point coord, ctypes.c_float tolerance, ctypes.c_int connectivity8, ctypes.c_float replaceValue)
    addfunc(lib, "imaqMagicWand", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, Point, ctypes.c_float, ctypes.c_int, ctypes.c_float],
            argnames = ["dest", "source", "coord", "tolerance", "connectivity8", "replaceValue"] )
    #  ctypes.c_int imaqMultithreshold(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ThresholdData) ranges, ctypes.c_int numRanges)
    addfunc(lib, "imaqMultithreshold", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ThresholdData), ctypes.c_int],
            argnames = ["dest", "source", "ranges", "numRanges"] )
    #  ctypes.c_int imaqThreshold(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_float rangeMin, ctypes.c_float rangeMax, ctypes.c_int useNewValue, ctypes.c_float newValue)
    addfunc(lib, "imaqThreshold", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.c_int, ctypes.c_float],
            argnames = ["dest", "source", "rangeMin", "rangeMax", "useNewValue", "newValue"] )
    #  ctypes.c_int imaqDispose(ctypes.c_void_p object)
    addfunc(lib, "imaqDispose", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["object"] )
    #  ctypes.POINTER(CircleMatch) imaqDetectCircles(ctypes.c_void_p image, ctypes.POINTER(CircleDescriptor) circleDescriptor, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(ShapeDetectionOptions) shapeDetectionOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatchesReturned)
    addfunc(lib, "imaqDetectCircles", restype = ctypes.POINTER(CircleMatch),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CircleDescriptor), ctypes.POINTER(CurveOptions), ctypes.POINTER(ShapeDetectionOptions), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "circleDescriptor", "curveOptions", "shapeDetectionOptions", "roi", "numMatchesReturned"] )
    #  ctypes.POINTER(EllipseMatch) imaqDetectEllipses(ctypes.c_void_p image, ctypes.POINTER(EllipseDescriptor) ellipseDescriptor, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(ShapeDetectionOptions) shapeDetectionOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatchesReturned)
    addfunc(lib, "imaqDetectEllipses", restype = ctypes.POINTER(EllipseMatch),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(EllipseDescriptor), ctypes.POINTER(CurveOptions), ctypes.POINTER(ShapeDetectionOptions), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "ellipseDescriptor", "curveOptions", "shapeDetectionOptions", "roi", "numMatchesReturned"] )
    #  ctypes.POINTER(LineMatch) imaqDetectLines(ctypes.c_void_p image, ctypes.POINTER(LineDescriptor) lineDescriptor, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(ShapeDetectionOptions) shapeDetectionOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatchesReturned)
    addfunc(lib, "imaqDetectLines", restype = ctypes.POINTER(LineMatch),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(LineDescriptor), ctypes.POINTER(CurveOptions), ctypes.POINTER(ShapeDetectionOptions), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "lineDescriptor", "curveOptions", "shapeDetectionOptions", "roi", "numMatchesReturned"] )
    #  ctypes.POINTER(RectangleMatch) imaqDetectRectangles(ctypes.c_void_p image, ctypes.POINTER(RectangleDescriptor) rectangleDescriptor, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(ShapeDetectionOptions) shapeDetectionOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatchesReturned)
    addfunc(lib, "imaqDetectRectangles", restype = ctypes.POINTER(RectangleMatch),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(RectangleDescriptor), ctypes.POINTER(CurveOptions), ctypes.POINTER(ShapeDetectionOptions), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "rectangleDescriptor", "curveOptions", "shapeDetectionOptions", "roi", "numMatchesReturned"] )
    #  ctypes.POINTER(FeatureData) imaqGetGeometricFeaturesFromCurves(ctypes.POINTER(Curve) curves, ctypes.c_uint numCurves, ctypes.POINTER(ctypes.c_int) featureTypes, ctypes.c_uint numFeatureTypes, ctypes.POINTER(ctypes.c_uint) numFeatures)
    addfunc(lib, "imaqGetGeometricFeaturesFromCurves", restype = ctypes.POINTER(FeatureData),
            argtypes = [ctypes.POINTER(Curve), ctypes.c_uint, ctypes.POINTER(ctypes.c_int), ctypes.c_uint, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["curves", "numCurves", "featureTypes", "numFeatureTypes", "numFeatures"] )
    #  ctypes.POINTER(FeatureData) imaqGetGeometricTemplateFeatureInfo(ctypes.c_void_p pattern, ctypes.POINTER(ctypes.c_uint) numFeatures)
    addfunc(lib, "imaqGetGeometricTemplateFeatureInfo", restype = ctypes.POINTER(FeatureData),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["pattern", "numFeatures"] )
    #  ctypes.c_int imaqLearnColorPattern(ctypes.c_void_p image, ctypes.POINTER(LearnColorPatternOptions) options)
    addfunc(lib, "imaqLearnColorPattern", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(LearnColorPatternOptions)],
            argnames = ["image", "options"] )
    #  ctypes.c_int imaqLearnGeometricPattern(ctypes.c_void_p image, PointFloat originOffset, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(LearnGeometricPatternAdvancedOptions) advancedLearnOptions, ctypes.c_void_p mask)
    addfunc(lib, "imaqLearnGeometricPattern", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, PointFloat, ctypes.POINTER(CurveOptions), ctypes.POINTER(LearnGeometricPatternAdvancedOptions), ctypes.c_void_p],
            argnames = ["image", "originOffset", "curveOptions", "advancedLearnOptions", "mask"] )
    #  ctypes.c_void_p imaqLearnMultipleGeometricPatterns(ctypes.POINTER(ctypes.c_void_p) patterns, ctypes.c_uint numberOfPatterns, ctypes.POINTER(String255) labels)
    addfunc(lib, "imaqLearnMultipleGeometricPatterns", restype = ctypes.c_void_p,
            argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint, ctypes.POINTER(String255)],
            argnames = ["patterns", "numberOfPatterns", "labels"] )
    #  ctypes.c_int imaqLearnPattern3(ctypes.c_void_p image, ctypes.c_int learningMode, ctypes.POINTER(LearnPatternAdvancedOptions) advancedOptions, ctypes.c_void_p mask)
    addfunc(lib, "imaqLearnPattern3", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(LearnPatternAdvancedOptions), ctypes.c_void_p],
            argnames = ["image", "learningMode", "advancedOptions", "mask"] )
    #  ctypes.POINTER(PatternMatch) imaqMatchColorPattern(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(MatchColorPatternOptions) options, Rect searchRect, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchColorPattern", restype = ctypes.POINTER(PatternMatch),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(MatchColorPatternOptions), Rect, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "options", "searchRect", "numMatches"] )
    #  ctypes.POINTER(GeometricPatternMatch2) imaqMatchGeometricPattern2(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(MatchGeometricPatternOptions) matchOptions, ctypes.POINTER(MatchGeometricPatternAdvancedOptions2) advancedMatchOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchGeometricPattern2", restype = ctypes.POINTER(GeometricPatternMatch2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CurveOptions), ctypes.POINTER(MatchGeometricPatternOptions), ctypes.POINTER(MatchGeometricPatternAdvancedOptions2), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "curveOptions", "matchOptions", "advancedMatchOptions", "roi", "numMatches"] )
    #  ctypes.POINTER(GeometricPatternMatch2) imaqMatchMultipleGeometricPatterns(ctypes.c_void_p image, ctypes.c_void_p multiplePattern, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchMultipleGeometricPatterns", restype = ctypes.POINTER(GeometricPatternMatch2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "multiplePattern", "roi", "numMatches"] )
    #  ctypes.c_void_p imaqReadMultipleGeometricPatternFile(ctypes.c_char_p fileName, String255 description)
    addfunc(lib, "imaqReadMultipleGeometricPatternFile", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_char_p, String255],
            argnames = ["fileName", "description"] )
    #  ctypes.POINTER(PatternMatch) imaqRefineMatches(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(PatternMatch) candidatesIn, ctypes.c_int numCandidatesIn, ctypes.POINTER(MatchPatternOptions) options, ctypes.POINTER(MatchPatternAdvancedOptions) advancedOptions, ctypes.POINTER(ctypes.c_int) numCandidatesOut)
    addfunc(lib, "imaqRefineMatches", restype = ctypes.POINTER(PatternMatch),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(PatternMatch), ctypes.c_int, ctypes.POINTER(MatchPatternOptions), ctypes.POINTER(MatchPatternAdvancedOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "candidatesIn", "numCandidatesIn", "options", "advancedOptions", "numCandidatesOut"] )
    #  ctypes.c_int imaqSetMultipleGeometricPatternsOptions(ctypes.c_void_p multiplePattern, ctypes.c_char_p label, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(MatchGeometricPatternOptions) matchOptions, ctypes.POINTER(MatchGeometricPatternAdvancedOptions2) advancedMatchOptions)
    addfunc(lib, "imaqSetMultipleGeometricPatternsOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(CurveOptions), ctypes.POINTER(MatchGeometricPatternOptions), ctypes.POINTER(MatchGeometricPatternAdvancedOptions2)],
            argnames = ["multiplePattern", "label", "curveOptions", "matchOptions", "advancedMatchOptions"] )
    #  ctypes.c_int imaqWriteMultipleGeometricPatternFile(ctypes.c_void_p multiplePattern, ctypes.c_char_p fileName, ctypes.c_char_p description)
    addfunc(lib, "imaqWriteMultipleGeometricPatternFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["multiplePattern", "fileName", "description"] )
    #  ctypes.POINTER(GeometricPatternMatch3) imaqMatchGeometricPattern5(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(MatchGeometricPatternOptions) matchOptions, ctypes.POINTER(GeometricAdvancedSetupDataOption) advancedMatchOptions, ctypes.c_uint numadvancedMatchOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_size_t) numMatches)
    addfunc(lib, "imaqMatchGeometricPattern5", restype = ctypes.POINTER(GeometricPatternMatch3),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(MatchGeometricPatternOptions), ctypes.POINTER(GeometricAdvancedSetupDataOption), ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["image", "pattern", "matchOptions", "advancedMatchOptions", "numadvancedMatchOptions", "roi", "numMatches"] )
    #  ctypes.c_int imaqLearnGeometricPattern2(ctypes.c_void_p image, PointFloat originOffset, ctypes.c_double angleOffset, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(LearnGeometricPatternAdvancedOptions2) advancedLearnOptions, ctypes.c_void_p mask)
    addfunc(lib, "imaqLearnGeometricPattern2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, PointFloat, ctypes.c_double, ctypes.POINTER(CurveOptions), ctypes.POINTER(LearnGeometricPatternAdvancedOptions2), ctypes.c_void_p],
            argnames = ["image", "originOffset", "angleOffset", "curveOptions", "advancedLearnOptions", "mask"] )
    #  ctypes.c_int imaqLearnGeometricPattern3(ctypes.c_void_p image, PointFloat originOffset, ctypes.c_double angleOffset, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(LearnGeometricPatternAdvancedOptions2) advancedLearnOptions, ctypes.c_void_p mask, ctypes.c_void_p weightmap)
    addfunc(lib, "imaqLearnGeometricPattern3", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, PointFloat, ctypes.c_double, ctypes.POINTER(CurveOptions), ctypes.POINTER(LearnGeometricPatternAdvancedOptions2), ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["image", "originOffset", "angleOffset", "curveOptions", "advancedLearnOptions", "mask", "weightmap"] )
    #  ctypes.c_int imaqSetAdvancedGeometricPatternOptions(ctypes.c_void_p image, ctypes.POINTER(GeometricAdvancedSetupDataOption) advancedOptionsHandle, ctypes.c_uint numAdvancedOptions)
    addfunc(lib, "imaqSetAdvancedGeometricPatternOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(GeometricAdvancedSetupDataOption), ctypes.c_uint],
            argnames = ["image", "advancedOptionsHandle", "numAdvancedOptions"] )
    #  ctypes.POINTER(GeometricMatchTemplateInformation) imaqGetGeometricPatternTemplateInformation(ctypes.c_void_p templateImage, ctypes.c_void_p maskImage, ctypes.c_void_p weightMap)
    addfunc(lib, "imaqGetGeometricPatternTemplateInformation", restype = ctypes.POINTER(GeometricMatchTemplateInformation),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["templateImage", "maskImage", "weightMap"] )
    #  ctypes.POINTER(PatternMatch) imaqMatchPattern3(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(MatchPatternOptions) options, ctypes.POINTER(MatchPatternAdvancedOptions) advancedOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchPattern3", restype = ctypes.POINTER(PatternMatch),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(MatchPatternOptions), ctypes.POINTER(MatchPatternAdvancedOptions), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "options", "advancedOptions", "roi", "numMatches"] )
    #  ctypes.c_int imaqLearnPattern6(ctypes.c_void_p templateImage, ctypes.c_void_p weightMap, ctypes.c_void_p maskImage, ctypes.c_int matchingAlgorithm, ctypes.POINTER(RotationAngleRange) rotationAngleRange, ctypes.POINTER(PMLearnAdvancedSetupDataOption) advancedOptionsHandle, ctypes.c_uint numAdvancedOptions, ctypes.POINTER(TemplateReport) templateReport)
    addfunc(lib, "imaqLearnPattern6", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(RotationAngleRange), ctypes.POINTER(PMLearnAdvancedSetupDataOption), ctypes.c_uint, ctypes.POINTER(TemplateReport)],
            argnames = ["templateImage", "weightMap", "maskImage", "matchingAlgorithm", "rotationAngleRange", "advancedOptionsHandle", "numAdvancedOptions", "templateReport"] )
    #  ctypes.POINTER(PatternMatchReport) imaqMatchPattern4(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.c_int matchingAlgorithm, ctypes.c_int numRequestedMatches, ctypes.c_float minScore, ctypes.POINTER(RotationAngleRange) rotationAngleRange, ctypes.c_int numRotationAngleRange, ctypes.c_void_p roi, ctypes.POINTER(PMMatchAdvancedSetupDataOption) advancedOptionsHandle, ctypes.c_uint numAdvancedOptions, ctypes.POINTER(ctypes.c_int) numMatchesFound)
    addfunc(lib, "imaqMatchPattern4", restype = ctypes.POINTER(PatternMatchReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.POINTER(RotationAngleRange), ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(PMMatchAdvancedSetupDataOption), ctypes.c_uint, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "matchingAlgorithm", "numRequestedMatches", "minScore", "rotationAngleRange", "numRotationAngleRange", "roi", "advancedOptionsHandle", "numAdvancedOptions", "numMatchesFound"] )
    #  ctypes.c_int imaqSetAdvancedMatchPatternOptions(ctypes.c_void_p image, ctypes.c_int algorithm, ctypes.POINTER(PMMatchAdvancedSetupDataOption) advancedOptionsHandle, ctypes.c_uint numAdvancedOptions)
    addfunc(lib, "imaqSetAdvancedMatchPatternOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(PMMatchAdvancedSetupDataOption), ctypes.c_uint],
            argnames = ["image", "algorithm", "advancedOptionsHandle", "numAdvancedOptions"] )
    #  ctypes.c_int imaqGetTemplateInformation(ctypes.c_void_p templateImage, ctypes.c_void_p maskImage, ctypes.c_int matchingAlgorithm, ctypes.POINTER(PyramidInfoStruct) pyramidInfo, ctypes.POINTER(MatchOffsetInfoStruct) matchOffsetInfo)
    addfunc(lib, "imaqGetTemplateInformation", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(PyramidInfoStruct), ctypes.POINTER(MatchOffsetInfoStruct)],
            argnames = ["templateImage", "maskImage", "matchingAlgorithm", "pyramidInfo", "matchOffsetInfo"] )
    #  ctypes.c_int imaqGetTemplateInformation2(ctypes.c_void_p templateImage, ctypes.c_void_p maskImage, ctypes.c_void_p weightMap, ctypes.c_int matchingAlgorithm, ctypes.POINTER(PyramidInfoStruct) pyramidInfo, ctypes.POINTER(MatchOffsetInfoStruct) matchOffsetInfo)
    addfunc(lib, "imaqGetTemplateInformation2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(PyramidInfoStruct), ctypes.POINTER(MatchOffsetInfoStruct)],
            argnames = ["templateImage", "maskImage", "weightMap", "matchingAlgorithm", "pyramidInfo", "matchOffsetInfo"] )
    #  ctypes.POINTER(PatternMatchTemplateInformation) imaqGetTemplateInformation3(ctypes.c_void_p templateImage, ctypes.c_void_p maskImage, ctypes.c_void_p weightMap, ctypes.c_int matchingAlgorithm)
    addfunc(lib, "imaqGetTemplateInformation3", restype = ctypes.POINTER(PatternMatchTemplateInformation),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["templateImage", "maskImage", "weightMap", "matchingAlgorithm"] )
    #  ctypes.c_int imaqCalculateDefectMap(ctypes.c_void_p srcImage, ctypes.c_int windowSize, ctypes.POINTER(ctypes.c_void_p) defectImages, ctypes.c_uint numOfImages)
    addfunc(lib, "imaqCalculateDefectMap", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint],
            argnames = ["srcImage", "windowSize", "defectImages", "numOfImages"] )
    #  ctypes.c_int imaqSetPresetMatchOptions(ctypes.c_void_p image, ctypes.c_int function, ctypes.POINTER(PresetOption) presetOptionsHandle, ctypes.c_uint numPresetOptions)
    addfunc(lib, "imaqSetPresetMatchOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(PresetOption), ctypes.c_uint],
            argnames = ["image", "function", "presetOptionsHandle", "numPresetOptions"] )
    #  ctypes.c_int imaqCopyCalibrationInfo2(ctypes.c_void_p dest, ctypes.c_void_p source, Point offset)
    addfunc(lib, "imaqCopyCalibrationInfo2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, Point],
            argnames = ["dest", "source", "offset"] )
    #  ctypes.c_int imaqCorrectCalibratedImage(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int fill, ctypes.c_int method, ctypes.c_void_p roi)
    addfunc(lib, "imaqCorrectCalibratedImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p],
            argnames = ["dest", "source", "fill", "method", "roi"] )
    #  ctypes.POINTER(CalibrationInfo) imaqGetCalibrationInfo2(ctypes.c_void_p image)
    addfunc(lib, "imaqGetCalibrationInfo2", restype = ctypes.POINTER(CalibrationInfo),
            argtypes = [ctypes.c_void_p],
            argnames = ["image"] )
    #  ctypes.POINTER(CalibrationInfo) imaqGetCalibrationInfo3(ctypes.c_void_p image, ctypes.c_uint isGetErrorMap)
    addfunc(lib, "imaqGetCalibrationInfo3", restype = ctypes.POINTER(CalibrationInfo),
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["image", "isGetErrorMap"] )
    #  ctypes.c_int imaqLearnCalibrationGrid(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(LearnCalibrationOptions) options, ctypes.POINTER(GridDescriptor) grid, ctypes.POINTER(CoordinateSystem) system, ctypes.POINTER(RangeFloat) range, ctypes.POINTER(ctypes.c_float) quality)
    addfunc(lib, "imaqLearnCalibrationGrid", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(LearnCalibrationOptions), ctypes.POINTER(GridDescriptor), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(RangeFloat), ctypes.POINTER(ctypes.c_float)],
            argnames = ["image", "roi", "options", "grid", "system", "range", "quality"] )
    #  ctypes.c_int imaqLearnCalibrationPoints(ctypes.c_void_p image, ctypes.POINTER(CalibrationPoints) points, ctypes.c_void_p roi, ctypes.POINTER(LearnCalibrationOptions) options, ctypes.POINTER(GridDescriptor) grid, ctypes.POINTER(CoordinateSystem) system, ctypes.POINTER(ctypes.c_float) quality)
    addfunc(lib, "imaqLearnCalibrationPoints", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CalibrationPoints), ctypes.c_void_p, ctypes.POINTER(LearnCalibrationOptions), ctypes.POINTER(GridDescriptor), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(ctypes.c_float)],
            argnames = ["image", "points", "roi", "options", "grid", "system", "quality"] )
    #  ctypes.c_int imaqSetCoordinateSystem(ctypes.c_void_p image, ctypes.POINTER(CoordinateSystem) system)
    addfunc(lib, "imaqSetCoordinateSystem", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CoordinateSystem)],
            argnames = ["image", "system"] )
    #  ctypes.c_int imaqSetSimpleCalibration(ctypes.c_void_p image, ctypes.c_int method, ctypes.c_int learnTable, ctypes.POINTER(GridDescriptor) grid, ctypes.POINTER(CoordinateSystem) system)
    addfunc(lib, "imaqSetSimpleCalibration", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(GridDescriptor), ctypes.POINTER(CoordinateSystem)],
            argnames = ["image", "method", "learnTable", "grid", "system"] )
    #  ctypes.POINTER(TransformReport) imaqTransformPixelToRealWorld(ctypes.c_void_p image, ctypes.POINTER(PointFloat) pixelCoordinates, ctypes.c_int numCoordinates)
    addfunc(lib, "imaqTransformPixelToRealWorld", restype = ctypes.POINTER(TransformReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(PointFloat), ctypes.c_int],
            argnames = ["image", "pixelCoordinates", "numCoordinates"] )
    #  ctypes.POINTER(TransformReport) imaqTransformRealWorldToPixel(ctypes.c_void_p image, ctypes.POINTER(PointFloat) realWorldCoordinates, ctypes.c_int numCoordinates)
    addfunc(lib, "imaqTransformRealWorldToPixel", restype = ctypes.POINTER(TransformReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(PointFloat), ctypes.c_int],
            argnames = ["image", "realWorldCoordinates", "numCoordinates"] )
    #  ctypes.POINTER(CalibrationReferencePoints) imaqCalibrationTargetToPoints2(ctypes.c_void_p image, ctypes.c_void_p mask, ctypes.c_void_p roi, ctypes.POINTER(GridDescriptor) gridDescriptor, ctypes.POINTER(MaxGridSize) maxGridSize)
    addfunc(lib, "imaqCalibrationTargetToPoints2", restype = ctypes.POINTER(CalibrationReferencePoints),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(GridDescriptor), ctypes.POINTER(MaxGridSize)],
            argnames = ["image", "mask", "roi", "gridDescriptor", "maxGridSize"] )
    #  ctypes.c_int imaqSetSimpleCalibration2(ctypes.c_void_p image, ctypes.POINTER(GridDescriptor) gridDescriptor)
    addfunc(lib, "imaqSetSimpleCalibration2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(GridDescriptor)],
            argnames = ["image", "gridDescriptor"] )
    #  ctypes.c_int imaqCalibrationSetAxisInfo(ctypes.c_void_p image, ctypes.POINTER(CoordinateSystem) axisInfo)
    addfunc(lib, "imaqCalibrationSetAxisInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CoordinateSystem)],
            argnames = ["image", "axisInfo"] )
    #  ctypes.c_int imaqCalibrationSetAxisInfoByReferencePoints(ctypes.c_void_p image, ctypes.POINTER(PointDouble) pixelCoordinates, ctypes.c_int numPixelCoordinates, ctypes.POINTER(PointDouble) realCoordinates, ctypes.c_int numRealCoordinates)
    addfunc(lib, "imaqCalibrationSetAxisInfoByReferencePoints", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(PointDouble), ctypes.c_int, ctypes.POINTER(PointDouble), ctypes.c_int],
            argnames = ["image", "pixelCoordinates", "numPixelCoordinates", "realCoordinates", "numRealCoordinates"] )
    #  ctypes.c_int imaqCalibrationGetThumbnailImage(ctypes.c_void_p templateImage, ctypes.c_void_p image, ctypes.c_int type, ctypes.c_uint index)
    addfunc(lib, "imaqCalibrationGetThumbnailImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_uint],
            argnames = ["templateImage", "image", "type", "index"] )
    #  ctypes.POINTER(GetCalibrationInfoReport) imaqCalibrationGetCalibrationInfo(ctypes.c_void_p image, ctypes.c_uint isGetErrorMap)
    addfunc(lib, "imaqCalibrationGetCalibrationInfo", restype = ctypes.POINTER(GetCalibrationInfoReport),
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["image", "isGetErrorMap"] )
    #  ctypes.POINTER(GetCameraParametersReport) imaqCalibrationGetCameraParameters(ctypes.c_void_p templateImage)
    addfunc(lib, "imaqCalibrationGetCameraParameters", restype = ctypes.POINTER(GetCameraParametersReport),
            argtypes = [ctypes.c_void_p],
            argnames = ["templateImage"] )
    #  ctypes.c_int imaqCalibrationCompactInformation(ctypes.c_void_p image)
    addfunc(lib, "imaqCalibrationCompactInformation", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["image"] )
    #  ctypes.c_int imaqLearnPerspectiveCalibration(ctypes.c_void_p templateImage, ctypes.c_void_p image, ctypes.POINTER(CalibrationReferencePoints) referencePoints)
    addfunc(lib, "imaqLearnPerspectiveCalibration", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CalibrationReferencePoints)],
            argnames = ["templateImage", "image", "referencePoints"] )
    #  ctypes.c_int imaqLearnMicroPlaneCalibration(ctypes.c_void_p templateImage, ctypes.c_void_p image, ctypes.POINTER(CalibrationReferencePoints) referencePoints)
    addfunc(lib, "imaqLearnMicroPlaneCalibration", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CalibrationReferencePoints)],
            argnames = ["templateImage", "image", "referencePoints"] )
    #  ctypes.POINTER(InternalParameters) imaqLearnCameraModel(ctypes.c_void_p templateImage, ctypes.c_void_p image, ctypes.POINTER(CalibrationReferencePoints) referencePoints, ctypes.POINTER(CalibrationModelSetup) cameraModelSetup, ctypes.c_int isAddPointsAndLearn)
    addfunc(lib, "imaqLearnCameraModel", restype = ctypes.POINTER(InternalParameters),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CalibrationReferencePoints), ctypes.POINTER(CalibrationModelSetup), ctypes.c_int],
            argnames = ["templateImage", "image", "referencePoints", "cameraModelSetup", "isAddPointsAndLearn"] )
    #  ctypes.POINTER(InternalParameters) imaqLearnCameraModel2(ctypes.c_void_p templateImage, ctypes.c_void_p image, ctypes.POINTER(CalibrationReferencePoints) referencePoints, ctypes.POINTER(CalibrationModelSetup) cameraModelSetup, ctypes.c_int isAddPointsAndLearn)
    addfunc(lib, "imaqLearnCameraModel2", restype = ctypes.POINTER(InternalParameters),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CalibrationReferencePoints), ctypes.POINTER(CalibrationModelSetup), ctypes.c_int],
            argnames = ["templateImage", "image", "referencePoints", "cameraModelSetup", "isAddPointsAndLearn"] )
    #  ctypes.c_int imaqLearnDistortionModel(ctypes.c_void_p templateImage, ctypes.c_void_p image, ctypes.POINTER(CalibrationReferencePoints) referencePoints, ctypes.POINTER(CalibrationModelSetup) distortionModelSetup, ctypes.c_int isAddPointsAndLearn)
    addfunc(lib, "imaqLearnDistortionModel", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CalibrationReferencePoints), ctypes.POINTER(CalibrationModelSetup), ctypes.c_int],
            argnames = ["templateImage", "image", "referencePoints", "distortionModelSetup", "isAddPointsAndLearn"] )
    #  ctypes.c_int imaqLearnDistortionModel2(ctypes.c_void_p templateImage, ctypes.c_void_p image, ctypes.POINTER(CalibrationReferencePoints) referencePoints, ctypes.POINTER(CalibrationModelSetup) distortionModelSetup, ctypes.c_int isAddPointsAndLearn)
    addfunc(lib, "imaqLearnDistortionModel2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CalibrationReferencePoints), ctypes.POINTER(CalibrationModelSetup), ctypes.c_int],
            argnames = ["templateImage", "image", "referencePoints", "distortionModelSetup", "isAddPointsAndLearn"] )
    #  ctypes.c_int imaqCalibrationCorrectionLearnSetup2(ctypes.c_void_p templateImage, ctypes.POINTER(CalibrationCorrectionLearnSetupInfo) setupInfo, ctypes.c_void_p roi, ctypes.c_int isApplyCalibrationAxis)
    addfunc(lib, "imaqCalibrationCorrectionLearnSetup2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CalibrationCorrectionLearnSetupInfo), ctypes.c_void_p, ctypes.c_int],
            argnames = ["templateImage", "setupInfo", "roi", "isApplyCalibrationAxis"] )
    #  ctypes.c_void_p imaqCreateCharSet()
    addfunc(lib, "imaqCreateCharSet", restype = ctypes.c_void_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int imaqDeleteChar(ctypes.c_void_p set, ctypes.c_int index)
    addfunc(lib, "imaqDeleteChar", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["set", "index"] )
    #  ctypes.c_int imaqGetCharCount(ctypes.c_void_p set)
    addfunc(lib, "imaqGetCharCount", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["set"] )
    #  ctypes.POINTER(CharInfo2) imaqGetCharInfo2(ctypes.c_void_p set, ctypes.c_int index)
    addfunc(lib, "imaqGetCharInfo2", restype = ctypes.POINTER(CharInfo2),
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["set", "index"] )
    #  ctypes.c_int imaqReadOCRFile2(ctypes.c_char_p fileName, ctypes.c_void_p set, String255 setDescription, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions2) processingOptions, ctypes.POINTER(OCRSpacingOptions2) spacingOptions)
    addfunc(lib, "imaqReadOCRFile2", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_void_p, String255, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions2), ctypes.POINTER(OCRSpacingOptions2)],
            argnames = ["fileName", "set", "setDescription", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.POINTER(ReadTextReport4) imaqReadText4(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.c_void_p roi, ctypes.c_int numberOfLinesRequested, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions2) processingOptions, ctypes.POINTER(OCRSpacingOptions2) spacingOptions)
    addfunc(lib, "imaqReadText4", restype = ctypes.POINTER(ReadTextReport4),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions2), ctypes.POINTER(OCRSpacingOptions2)],
            argnames = ["image", "set", "roi", "numberOfLinesRequested", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.c_int imaqRenameChar(ctypes.c_void_p set, ctypes.c_int index, ctypes.c_char_p newCharValue)
    addfunc(lib, "imaqRenameChar", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p],
            argnames = ["set", "index", "newCharValue"] )
    #  ctypes.c_int imaqSetReferenceChar(ctypes.c_void_p set, ctypes.c_int index, ctypes.c_int isReferenceChar)
    addfunc(lib, "imaqSetReferenceChar", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["set", "index", "isReferenceChar"] )
    #  ctypes.c_int imaqTrainChars2(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.c_int index, ctypes.c_char_p charValue, ctypes.c_void_p roi, ctypes.POINTER(OCRProcessingOptions2) processingOptions, ctypes.POINTER(OCRSpacingOptions2) spacingOptions)
    addfunc(lib, "imaqTrainChars2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p, ctypes.POINTER(OCRProcessingOptions2), ctypes.POINTER(OCRSpacingOptions2)],
            argnames = ["image", "set", "index", "charValue", "roi", "processingOptions", "spacingOptions"] )
    #  ctypes.POINTER(ctypes.c_int) imaqVerifyPatterns(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.POINTER(String255) expectedPatterns, ctypes.c_int patternCount, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numScores)
    addfunc(lib, "imaqVerifyPatterns", restype = ctypes.POINTER(ctypes.c_int),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(String255), ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "set", "expectedPatterns", "patternCount", "roi", "numScores"] )
    #  ctypes.POINTER(ctypes.c_int) imaqVerifyText(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.c_char_p expectedString, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numScores)
    addfunc(lib, "imaqVerifyText", restype = ctypes.POINTER(ctypes.c_int),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "set", "expectedString", "roi", "numScores"] )
    #  ctypes.c_int imaqWriteOCRFile2(ctypes.c_char_p fileName, ctypes.c_void_p set, ctypes.c_char_p setDescription, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions2) processingOptions, ctypes.POINTER(OCRSpacingOptions2) spacingOptions)
    addfunc(lib, "imaqWriteOCRFile2", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions2), ctypes.POINTER(OCRSpacingOptions2)],
            argnames = ["fileName", "set", "setDescription", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.POINTER(ClampMax2Report) imaqClampMax3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(CurveOptions) curveSettings, ctypes.POINTER(ClampSettings) clampSettings, ctypes.POINTER(ClampOverlaySettings) clampOverlaySettings)
    addfunc(lib, "imaqClampMax3", restype = ctypes.POINTER(ClampMax2Report),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CurveOptions), ctypes.POINTER(ClampSettings), ctypes.POINTER(ClampOverlaySettings)],
            argnames = ["image", "roi", "baseSystem", "newSystem", "curveSettings", "clampSettings", "clampOverlaySettings"] )
    #  ctypes.POINTER(ExtractContourReport) imaqExtractContour(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.POINTER(CurveParameters) curveParams, ctypes.POINTER(ConnectionConstraint) connectionConstraintParams, ctypes.c_uint numOfConstraints, ctypes.c_int selection, ctypes.c_void_p contourImage)
    addfunc(lib, "imaqExtractContour", restype = ctypes.POINTER(ExtractContourReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(CurveParameters), ctypes.POINTER(ConnectionConstraint), ctypes.c_uint, ctypes.c_int, ctypes.c_void_p],
            argnames = ["image", "roi", "direction", "curveParams", "connectionConstraintParams", "numOfConstraints", "selection", "contourImage"] )
    #  ctypes.c_int imaqContourOverlay(ctypes.c_void_p image, ctypes.c_void_p contourImage, ctypes.POINTER(ContourOverlaySettings) pointsSettings, ctypes.POINTER(ContourOverlaySettings) eqnSettings, ctypes.c_char_p groupName)
    addfunc(lib, "imaqContourOverlay", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ContourOverlaySettings), ctypes.POINTER(ContourOverlaySettings), ctypes.c_char_p],
            argnames = ["image", "contourImage", "pointsSettings", "eqnSettings", "groupName"] )
    #  ctypes.POINTER(ContourComputeCurvatureReport) imaqContourComputeCurvature(ctypes.c_void_p contourImage, ctypes.c_uint kernel)
    addfunc(lib, "imaqContourComputeCurvature", restype = ctypes.POINTER(ContourComputeCurvatureReport),
            argtypes = [ctypes.c_void_p, ctypes.c_uint],
            argnames = ["contourImage", "kernel"] )
    #  ctypes.POINTER(CurvatureAnalysisReport) imaqContourClassifyCurvature(ctypes.c_void_p contourImage, ctypes.c_uint kernel, ctypes.POINTER(RangeLabel) curvatureClasses, ctypes.c_uint numCurvatureClasses)
    addfunc(lib, "imaqContourClassifyCurvature", restype = ctypes.POINTER(CurvatureAnalysisReport),
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(RangeLabel), ctypes.c_uint],
            argnames = ["contourImage", "kernel", "curvatureClasses", "numCurvatureClasses"] )
    #  ctypes.POINTER(ComputeDistancesReport) imaqContourComputeDistances(ctypes.c_void_p targetImage, ctypes.c_void_p templateImage, ctypes.POINTER(SetupMatchPatternData) matchSetupData, ctypes.c_uint smoothingKernel)
    addfunc(lib, "imaqContourComputeDistances", restype = ctypes.POINTER(ComputeDistancesReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(SetupMatchPatternData), ctypes.c_uint],
            argnames = ["targetImage", "templateImage", "matchSetupData", "smoothingKernel"] )
    #  ctypes.POINTER(ClassifyDistancesReport) imaqContourClassifyDistances(ctypes.c_void_p targetImage, ctypes.c_void_p templateImage, ctypes.POINTER(SetupMatchPatternData) matchSetupData, ctypes.c_uint smoothingKernel, ctypes.POINTER(RangeLabel) distanceRanges, ctypes.c_uint numDistanceRanges)
    addfunc(lib, "imaqContourClassifyDistances", restype = ctypes.POINTER(ClassifyDistancesReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(SetupMatchPatternData), ctypes.c_uint, ctypes.POINTER(RangeLabel), ctypes.c_uint],
            argnames = ["targetImage", "templateImage", "matchSetupData", "smoothingKernel", "distanceRanges", "numDistanceRanges"] )
    #  ctypes.POINTER(ContourInfoReport) imaqContourInfo(ctypes.c_void_p contourImage)
    addfunc(lib, "imaqContourInfo", restype = ctypes.POINTER(ContourInfoReport),
            argtypes = [ctypes.c_void_p],
            argnames = ["contourImage"] )
    #  ctypes.POINTER(SetupMatchPatternData) imaqContourSetupMatchPattern(ctypes.POINTER(MatchMode) matchMode, ctypes.c_uint enableSubPixelAccuracy, ctypes.POINTER(CurveParameters) curveParams, ctypes.c_uint useLearnCurveParameters, ctypes.POINTER(RangeSettingDouble) rangeSettings, ctypes.c_uint numRangeSettings)
    addfunc(lib, "imaqContourSetupMatchPattern", restype = ctypes.POINTER(SetupMatchPatternData),
            argtypes = [ctypes.POINTER(MatchMode), ctypes.c_uint, ctypes.POINTER(CurveParameters), ctypes.c_uint, ctypes.POINTER(RangeSettingDouble), ctypes.c_uint],
            argnames = ["matchMode", "enableSubPixelAccuracy", "curveParams", "useLearnCurveParameters", "rangeSettings", "numRangeSettings"] )
    #  ctypes.c_int imaqContourAdvancedSetupMatchPattern(ctypes.POINTER(SetupMatchPatternData) matchSetupData, ctypes.POINTER(GeometricAdvancedSetupDataOption) geometricOptions, ctypes.c_uint numGeometricOptions)
    addfunc(lib, "imaqContourAdvancedSetupMatchPattern", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(SetupMatchPatternData), ctypes.POINTER(GeometricAdvancedSetupDataOption), ctypes.c_uint],
            argnames = ["matchSetupData", "geometricOptions", "numGeometricOptions"] )
    #  ctypes.POINTER(ContourFitLineReport) imaqContourFitLine(ctypes.c_void_p image, ctypes.c_double pixelRadius)
    addfunc(lib, "imaqContourFitLine", restype = ctypes.POINTER(ContourFitLineReport),
            argtypes = [ctypes.c_void_p, ctypes.c_double],
            argnames = ["image", "pixelRadius"] )
    #  ctypes.POINTER(PartialCircle) imaqContourFitCircle(ctypes.c_void_p image, ctypes.c_double pixelRadius, ctypes.c_int rejectOutliers)
    addfunc(lib, "imaqContourFitCircle", restype = ctypes.POINTER(PartialCircle),
            argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int],
            argnames = ["image", "pixelRadius", "rejectOutliers"] )
    #  ctypes.POINTER(PartialEllipse) imaqContourFitEllipse(ctypes.c_void_p image, ctypes.c_double pixelRadius, ctypes.c_int rejectOutliers)
    addfunc(lib, "imaqContourFitEllipse", restype = ctypes.POINTER(PartialEllipse),
            argtypes = [ctypes.c_void_p, ctypes.c_double, ctypes.c_int],
            argnames = ["image", "pixelRadius", "rejectOutliers"] )
    #  ctypes.POINTER(ContourFitSplineReport) imaqContourFitSpline(ctypes.c_void_p image, ctypes.c_int degree, ctypes.c_int numberOfControlPoints)
    addfunc(lib, "imaqContourFitSpline", restype = ctypes.POINTER(ContourFitSplineReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["image", "degree", "numberOfControlPoints"] )
    #  ctypes.POINTER(ContourFitPolynomialReport) imaqContourFitPolynomial(ctypes.c_void_p image, ctypes.c_int order)
    addfunc(lib, "imaqContourFitPolynomial", restype = ctypes.POINTER(ContourFitPolynomialReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["image", "order"] )
    #  ctypes.POINTER(FindCircularEdgeReport) imaqFindCircularEdge2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(FindCircularEdgeOptions) edgeOptions, ctypes.POINTER(CircleFitOptions) circleFitOptions)
    addfunc(lib, "imaqFindCircularEdge2", restype = ctypes.POINTER(FindCircularEdgeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(FindCircularEdgeOptions), ctypes.POINTER(CircleFitOptions)],
            argnames = ["image", "roi", "baseSystem", "newSystem", "edgeOptions", "circleFitOptions"] )
    #  ctypes.POINTER(FindConcentricEdgeReport) imaqFindConcentricEdge2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(FindConcentricEdgeOptions) edgeOptions, ctypes.POINTER(ConcentricEdgeFitOptions) concentricEdgeFitOptions)
    addfunc(lib, "imaqFindConcentricEdge2", restype = ctypes.POINTER(FindConcentricEdgeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(FindConcentricEdgeOptions), ctypes.POINTER(ConcentricEdgeFitOptions)],
            argnames = ["image", "roi", "baseSystem", "newSystem", "edgeOptions", "concentricEdgeFitOptions"] )
    #  ctypes.c_int imaqGrayMorphologyReconstruct(ctypes.c_void_p dstImage, ctypes.c_void_p srcImage, ctypes.c_void_p markerImage, ctypes.POINTER(PointFloat) points, ctypes.c_int numOfPoints, ctypes.c_int operation, ctypes.POINTER(StructuringElement) structuringElement, ctypes.c_void_p roi)
    addfunc(lib, "imaqGrayMorphologyReconstruct", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.c_int, ctypes.POINTER(StructuringElement), ctypes.c_void_p],
            argnames = ["dstImage", "srcImage", "markerImage", "points", "numOfPoints", "operation", "structuringElement", "roi"] )
    #  ctypes.c_int imaqMorphologyReconstruct(ctypes.c_void_p dstImage, ctypes.c_void_p srcImage, ctypes.c_void_p markerImage, ctypes.POINTER(PointFloat) points, ctypes.c_int numOfPoints, ctypes.c_int operation, ctypes.c_int connectivity, ctypes.c_void_p roi)
    addfunc(lib, "imaqMorphologyReconstruct", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p],
            argnames = ["dstImage", "srcImage", "markerImage", "points", "numOfPoints", "operation", "connectivity", "roi"] )
    #  ctypes.c_int imaqDetectTextureDefect(ctypes.c_void_p session, ctypes.c_void_p destImage, ctypes.c_void_p srcImage, ctypes.c_void_p roi, ctypes.c_int initialStepSize, ctypes.c_int finalStepSize, ctypes.c_ubyte defectPixelValue, ctypes.c_double minClassificationScore)
    addfunc(lib, "imaqDetectTextureDefect", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_ubyte, ctypes.c_double],
            argnames = ["session", "destImage", "srcImage", "roi", "initialStepSize", "finalStepSize", "defectPixelValue", "minClassificationScore"] )
    #  ctypes.c_int imaqClassificationTextureDefectOptions(ctypes.c_void_p session, ctypes.POINTER(WindowSize) windowOptions, ctypes.POINTER(WaveletOptions) waveletOptions, ctypes.POINTER(ctypes.c_void_p) bandsUsed, ctypes.POINTER(ctypes.c_int) numBandsUsed, ctypes.POINTER(CooccurrenceOptions) cooccurrenceOptions, ctypes.c_ubyte setOperation)
    addfunc(lib, "imaqClassificationTextureDefectOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(WindowSize), ctypes.POINTER(WaveletOptions), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(CooccurrenceOptions), ctypes.c_ubyte],
            argnames = ["session", "windowOptions", "waveletOptions", "bandsUsed", "numBandsUsed", "cooccurrenceOptions", "setOperation"] )
    #  ctypes.c_int imaqCooccurrenceMatrix(ctypes.c_void_p srcImage, ctypes.c_void_p roi, ctypes.c_int levelPixel, ctypes.POINTER(DisplacementVector) displacementVec, ctypes.c_void_p featureOptionArray, ctypes.c_uint featureOptionArraySize, ctypes.POINTER(ctypes.c_void_p) cooccurrenceMatrixArray, ctypes.POINTER(ctypes.c_int) coocurrenceMatrixRows, ctypes.POINTER(ctypes.c_int) coocurrenceMatrixCols, ctypes.POINTER(ctypes.c_void_p) featureVectorArray, ctypes.POINTER(ctypes.c_int) featureVectorArraySize)
    addfunc(lib, "imaqCooccurrenceMatrix", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(DisplacementVector), ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_int)],
            argnames = ["srcImage", "roi", "levelPixel", "displacementVec", "featureOptionArray", "featureOptionArraySize", "cooccurrenceMatrixArray", "coocurrenceMatrixRows", "coocurrenceMatrixCols", "featureVectorArray", "featureVectorArraySize"] )
    #  ctypes.POINTER(ExtractTextureFeaturesReport) imaqExtractTextureFeatures(ctypes.c_void_p srcImage, ctypes.c_void_p roi, ctypes.POINTER(WindowSize) windowOptions, ctypes.POINTER(WaveletOptions) waveletOptions, ctypes.c_void_p waveletBands, ctypes.c_uint numWaveletBands, ctypes.POINTER(CooccurrenceOptions) cooccurrenceOptions, ctypes.c_ubyte useWindow)
    addfunc(lib, "imaqExtractTextureFeatures", restype = ctypes.POINTER(ExtractTextureFeaturesReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(WindowSize), ctypes.POINTER(WaveletOptions), ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(CooccurrenceOptions), ctypes.c_ubyte],
            argnames = ["srcImage", "roi", "windowOptions", "waveletOptions", "waveletBands", "numWaveletBands", "cooccurrenceOptions", "useWindow"] )
    #  ctypes.POINTER(WaveletBandsReport) imaqExtractWaveletBands(ctypes.c_void_p srcImage, ctypes.POINTER(WaveletOptions) waveletOptions, ctypes.c_void_p waveletBands, ctypes.c_uint numWaveletBands)
    addfunc(lib, "imaqExtractWaveletBands", restype = ctypes.POINTER(WaveletBandsReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(WaveletOptions), ctypes.c_void_p, ctypes.c_uint],
            argnames = ["srcImage", "waveletOptions", "waveletBands", "numWaveletBands"] )
    #  ctypes.c_void_p imaqMaskToROI(ctypes.c_void_p mask, ctypes.POINTER(ctypes.c_int) withinLimit)
    addfunc(lib, "imaqMaskToROI", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["mask", "withinLimit"] )
    #  ctypes.POINTER(ROIProfile) imaqROIProfile(ctypes.c_void_p image, ctypes.c_void_p roi)
    addfunc(lib, "imaqROIProfile", restype = ctypes.POINTER(ROIProfile),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["image", "roi"] )
    #  ctypes.c_int imaqROIToMask2(ctypes.c_void_p mask, ctypes.c_void_p roi, ctypes.c_int fillValue, ctypes.c_int backgoundValue, ctypes.c_void_p imageModel, ctypes.POINTER(ctypes.c_int) isROIinImageModelSpace)
    addfunc(lib, "imaqROIToMask2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["mask", "roi", "fillValue", "backgoundValue", "imageModel", "isROIinImageModelSpace"] )
    #  ctypes.c_int imaqTransformROI2(ctypes.c_void_p roi, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem)
    addfunc(lib, "imaqTransformROI2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem)],
            argnames = ["roi", "baseSystem", "newSystem"] )
    #  ctypes.POINTER(LabelToROIReport) imaqLabelToROI(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_uint) labelsIn, ctypes.c_uint numLabelsIn, ctypes.c_int maxNumVectors, ctypes.c_int isExternelEdges)
    addfunc(lib, "imaqLabelToROI", restype = ctypes.POINTER(LabelToROIReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint), ctypes.c_uint, ctypes.c_int, ctypes.c_int],
            argnames = ["image", "labelsIn", "numLabelsIn", "maxNumVectors", "isExternelEdges"] )
    #  ctypes.c_int imaqGrayMorphology2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int method, ctypes.POINTER(StructuringElement) structuringElement, ctypes.c_int numberOfIterations)
    addfunc(lib, "imaqGrayMorphology2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(StructuringElement), ctypes.c_int],
            argnames = ["dest", "source", "method", "structuringElement", "numberOfIterations"] )
    #  ctypes.c_int imaqAddClassifierSample(ctypes.c_void_p image, ctypes.c_void_p session, ctypes.c_void_p roi, ctypes.c_char_p sampleClass, ctypes.POINTER(ctypes.c_double) featureVector, ctypes.c_uint vectorSize)
    addfunc(lib, "imaqAddClassifierSample", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_double), ctypes.c_uint],
            argnames = ["image", "session", "roi", "sampleClass", "featureVector", "vectorSize"] )
    #  ctypes.POINTER(ClassifierReportAdvanced) imaqAdvanceClassify(ctypes.c_void_p image, ctypes.c_void_p session, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_double) featureVector, ctypes.c_uint vectorSize)
    addfunc(lib, "imaqAdvanceClassify", restype = ctypes.POINTER(ClassifierReportAdvanced),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.c_uint],
            argnames = ["image", "session", "roi", "featureVector", "vectorSize"] )
    #  ctypes.POINTER(SVMReport) imaqClassificationTrainSVM(ctypes.c_void_p session, ctypes.POINTER(SVMModelOptions) modelOptions, ctypes.POINTER(SVMKernelOptions) kernelOptions)
    addfunc(lib, "imaqClassificationTrainSVM", restype = ctypes.POINTER(SVMReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(SVMModelOptions), ctypes.POINTER(SVMKernelOptions)],
            argnames = ["session", "modelOptions", "kernelOptions"] )
    #  ctypes.POINTER(ClassifierReport) imaqClassify(ctypes.c_void_p image, ctypes.c_void_p session, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_double) featureVector, ctypes.c_uint vectorSize)
    addfunc(lib, "imaqClassify", restype = ctypes.POINTER(ClassifierReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_double), ctypes.c_uint],
            argnames = ["image", "session", "roi", "featureVector", "vectorSize"] )
    #  ctypes.c_void_p imaqCreateClassifier(ctypes.c_int type)
    addfunc(lib, "imaqCreateClassifier", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_int],
            argnames = ["type"] )
    #  ctypes.c_int imaqDeleteClassifierSample(ctypes.c_void_p session, ctypes.c_int index)
    addfunc(lib, "imaqDeleteClassifierSample", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["session", "index"] )
    #  ctypes.POINTER(ClassifierAccuracyReport) imaqGetClassifierAccuracy(ctypes.c_void_p session)
    addfunc(lib, "imaqGetClassifierAccuracy", restype = ctypes.POINTER(ClassifierAccuracyReport),
            argtypes = [ctypes.c_void_p],
            argnames = ["session"] )
    #  ctypes.POINTER(ClassifierSampleInfo) imaqGetClassifierSampleInfo(ctypes.c_void_p session, ctypes.c_int index, ctypes.POINTER(ctypes.c_int) numSamples)
    addfunc(lib, "imaqGetClassifierSampleInfo", restype = ctypes.POINTER(ClassifierSampleInfo),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["session", "index", "numSamples"] )
    #  ctypes.c_int imaqGetColorClassifierOptions(ctypes.c_void_p session, ctypes.POINTER(ColorOptions) options)
    addfunc(lib, "imaqGetColorClassifierOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ColorOptions)],
            argnames = ["session", "options"] )
    #  ctypes.c_int imaqGetNearestNeighborOptions(ctypes.c_void_p session, ctypes.POINTER(NearestNeighborOptions) options)
    addfunc(lib, "imaqGetNearestNeighborOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(NearestNeighborOptions)],
            argnames = ["session", "options"] )
    #  ctypes.c_int imaqGetParticleClassifierOptions2(ctypes.c_void_p session, ctypes.POINTER(ParticleClassifierPreprocessingOptions2) preprocessingOptions, ctypes.POINTER(ParticleClassifierOptions) options)
    addfunc(lib, "imaqGetParticleClassifierOptions2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ParticleClassifierPreprocessingOptions2), ctypes.POINTER(ParticleClassifierOptions)],
            argnames = ["session", "preprocessingOptions", "options"] )
    #  ctypes.c_void_p imaqReadClassifierFile(ctypes.c_void_p session, ctypes.c_char_p fileName, ctypes.c_int mode, ctypes.POINTER(ctypes.c_int) type, ctypes.POINTER(ctypes.c_int) engine, String255 description)
    addfunc(lib, "imaqReadClassifierFile", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), String255],
            argnames = ["session", "fileName", "mode", "type", "engine", "description"] )
    #  ctypes.c_int imaqRelabelClassifierSample(ctypes.c_void_p session, ctypes.c_int index, ctypes.c_char_p newClass)
    addfunc(lib, "imaqRelabelClassifierSample", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p],
            argnames = ["session", "index", "newClass"] )
    #  ctypes.c_int imaqSetParticleClassifierOptions2(ctypes.c_void_p session, ctypes.POINTER(ParticleClassifierPreprocessingOptions2) preprocessingOptions, ctypes.POINTER(ParticleClassifierOptions) options)
    addfunc(lib, "imaqSetParticleClassifierOptions2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ParticleClassifierPreprocessingOptions2), ctypes.POINTER(ParticleClassifierOptions)],
            argnames = ["session", "preprocessingOptions", "options"] )
    #  ctypes.c_int imaqSetColorClassifierOptions(ctypes.c_void_p session, ctypes.POINTER(ColorOptions) options)
    addfunc(lib, "imaqSetColorClassifierOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ColorOptions)],
            argnames = ["session", "options"] )
    #  ctypes.POINTER(NearestNeighborTrainingReport) imaqTrainNearestNeighborClassifier(ctypes.c_void_p session, ctypes.POINTER(NearestNeighborOptions) options)
    addfunc(lib, "imaqTrainNearestNeighborClassifier", restype = ctypes.POINTER(NearestNeighborTrainingReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(NearestNeighborOptions)],
            argnames = ["session", "options"] )
    #  ctypes.c_int imaqWriteClassifierFile(ctypes.c_void_p session, ctypes.c_char_p fileName, ctypes.c_int mode, String255 description)
    addfunc(lib, "imaqWriteClassifierFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, String255],
            argnames = ["session", "fileName", "mode", "description"] )
    #  ctypes.c_void_p imaq3DVisionCreateBinocularStereoSession()
    addfunc(lib, "imaq3DVisionCreateBinocularStereoSession", restype = ctypes.c_void_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int imaq3DVisionDisposeBincocularStereoSession(ctypes.c_void_p cSessionToDelete)
    addfunc(lib, "imaq3DVisionDisposeBincocularStereoSession", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["cSessionToDelete"] )
    #  ctypes.c_void_p imaq3DVisionReadBincocularStereoFile(ctypes.c_void_p cSessionToUpdate, ctypes.c_char_p chFilePath, String255 stDescription)
    addfunc(lib, "imaq3DVisionReadBincocularStereoFile", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, String255],
            argnames = ["cSessionToUpdate", "chFilePath", "stDescription"] )
    #  ctypes.c_int imaq3DVisionWriteBincocularStereoFile(ctypes.c_void_p cSessionReference, ctypes.c_char_p chFilePath, ctypes.c_int eOptions, String255 stDescriptionToWrite)
    addfunc(lib, "imaq3DVisionWriteBincocularStereoFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, String255],
            argnames = ["cSessionReference", "chFilePath", "eOptions", "stDescriptionToWrite"] )
    #  ctypes.c_int imaqVision3DLearnBincocularStereoCalibration(ctypes.c_void_p imgLeft, ctypes.c_void_p imgRight, ctypes.c_void_p cStereoSession, ctypes.POINTER(StereoLearnCalibQualiy) sStereoLearnCalibQualiy, ctypes.POINTER(StereoRtfSettings) sStereoRtfSettings)
    addfunc(lib, "imaqVision3DLearnBincocularStereoCalibration", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(StereoLearnCalibQualiy), ctypes.POINTER(StereoRtfSettings)],
            argnames = ["imgLeft", "imgRight", "cStereoSession", "sStereoLearnCalibQualiy", "sStereoRtfSettings"] )
    #  ctypes.POINTER(StereoCalibrationInfoReport) imaqVision3DBincocularGetCalibrationInfo(ctypes.c_void_p cSessionReference, ctypes.c_void_p sRoiLeft, ctypes.c_void_p sRoiRight)
    addfunc(lib, "imaqVision3DBincocularGetCalibrationInfo", restype = ctypes.POINTER(StereoCalibrationInfoReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["cSessionReference", "sRoiLeft", "sRoiRight"] )
    #  ctypes.c_int imaqVision3DBinocularStereoCorrespondenceUsingBM2(ctypes.c_void_p imgLeft, ctypes.c_void_p imgRight, ctypes.c_void_p imgDisparityMap, ctypes.c_void_p imgCostMap, ctypes.c_void_p cStereoSession, ctypes.c_int eCameraLocation, ctypes.POINTER(StereoPrefilterOptions) sPrefilterOptions, ctypes.POINTER(StereoBlockMatchingOptions) sBlockMatchingOptions, ctypes.POINTER(StereoPostfilterOptions) sPostfilterOptions, ctypes.c_int iProcessBandVal)
    addfunc(lib, "imaqVision3DBinocularStereoCorrespondenceUsingBM2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(StereoPrefilterOptions), ctypes.POINTER(StereoBlockMatchingOptions), ctypes.POINTER(StereoPostfilterOptions), ctypes.c_int],
            argnames = ["imgLeft", "imgRight", "imgDisparityMap", "imgCostMap", "cStereoSession", "eCameraLocation", "sPrefilterOptions", "sBlockMatchingOptions", "sPostfilterOptions", "iProcessBandVal"] )
    #  ctypes.c_int imaqVision3DBinocularStereoCorrespondenceUsingSGBM2(ctypes.c_void_p imgLeft, ctypes.c_void_p imgRight, ctypes.c_void_p imgDisparityMap, ctypes.c_void_p imgCostMap, ctypes.c_void_p cStereoSession, ctypes.c_int eCameraLocation, ctypes.c_int ePreCapFilter, ctypes.POINTER(StereoSGBlockMatchingOptions) sBlockMatchingOptions, ctypes.POINTER(StereoPostfilterOptions) sPostfilterOptions, ctypes.c_int iProcessBandVal)
    addfunc(lib, "imaqVision3DBinocularStereoCorrespondenceUsingSGBM2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(StereoSGBlockMatchingOptions), ctypes.POINTER(StereoPostfilterOptions), ctypes.c_int],
            argnames = ["imgLeft", "imgRight", "imgDisparityMap", "imgCostMap", "cStereoSession", "eCameraLocation", "ePreCapFilter", "sBlockMatchingOptions", "sPostfilterOptions", "iProcessBandVal"] )
    #  ctypes.c_int imaqVision3DBincocularStereoGetRectifiedImage(ctypes.c_void_p imgSource, ctypes.c_void_p imageDest, ctypes.c_void_p cStereoSession, ctypes.c_int eCameraLocation, ctypes.c_int eInterpolationType)
    addfunc(lib, "imaqVision3DBincocularStereoGetRectifiedImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["imgSource", "imageDest", "cStereoSession", "eCameraLocation", "eInterpolationType"] )
    #  ctypes.c_int imaqVision3DBincocularStereoGetDepthImage(ctypes.c_void_p imgSource, ctypes.c_void_p imageDest, ctypes.c_void_p imageErrorMap, ctypes.c_void_p cStereoSession, ctypes.c_int eCameraposition, ctypes.c_float fInvalidDisparityValue, StereoDepthControl sStereoDepthControl)
    addfunc(lib, "imaqVision3DBincocularStereoGetDepthImage", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_float, StereoDepthControl],
            argnames = ["imgSource", "imageDest", "imageErrorMap", "cStereoSession", "eCameraposition", "fInvalidDisparityValue", "sStereoDepthControl"] )
    #  ctypes.c_int imaqVision3DBincocularStereoGetDepthPlanes(ctypes.c_void_p imgSource, ctypes.c_void_p imgXPlane, ctypes.c_void_p imgYPlane, ctypes.c_void_p imgZPlane, ctypes.c_void_p cStereoSession, ctypes.c_int eCameraposition, ctypes.c_float fInvalidDisparityValue, StereoDepthControl sStereoDepthControl)
    addfunc(lib, "imaqVision3DBincocularStereoGetDepthPlanes", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_float, StereoDepthControl],
            argnames = ["imgSource", "imgXPlane", "imgYPlane", "imgZPlane", "cStereoSession", "eCameraposition", "fInvalidDisparityValue", "sStereoDepthControl"] )
    #  ctypes.POINTER(Pixelto3dCoordinatesReport) imaqVision3DBincocularConvertPixelTo3DCoordinates(ctypes.c_void_p cStereoSession, ctypes.c_void_p imgDisparity, ctypes.c_int eCameraposition, ctypes.POINTER(StereoPointDbl3D) sPtDbl3DOrigin, ctypes.POINTER(StereoPointDbl3D) sPtDbl3Rotation, ctypes.POINTER(StereoCoordPtFloat) sPixel2dPt, ctypes.POINTER(StereoCoordPtFloat) sPixel2dPoints, ctypes.c_uint iNumberofPixel2dPoints, ctypes.c_float fInvalidDisparityValue, ctypes.c_double dMinDepth, ctypes.c_double dMaxDepth)
    addfunc(lib, "imaqVision3DBincocularConvertPixelTo3DCoordinates", restype = ctypes.POINTER(Pixelto3dCoordinatesReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(StereoPointDbl3D), ctypes.POINTER(StereoPointDbl3D), ctypes.POINTER(StereoCoordPtFloat), ctypes.POINTER(StereoCoordPtFloat), ctypes.c_uint, ctypes.c_float, ctypes.c_double, ctypes.c_double],
            argnames = ["cStereoSession", "imgDisparity", "eCameraposition", "sPtDbl3DOrigin", "sPtDbl3Rotation", "sPixel2dPt", "sPixel2dPoints", "iNumberofPixel2dPoints", "fInvalidDisparityValue", "dMinDepth", "dMaxDepth"] )
    #  ctypes.c_int imaqGetMaxDisparityFromMinDepth(ctypes.POINTER(ctypes.c_double) a2QMarix, ctypes.POINTER(ctypes.c_int) iRows, ctypes.POINTER(ctypes.c_int) iCols, ctypes.c_double dMinDepth, ctypes.c_int dImageWidth, ctypes.POINTER(ctypes.c_int) iMaxDisparity, ctypes.POINTER(ctypes.c_double) dMinDepthCovered)
    addfunc(lib, "imaqGetMaxDisparityFromMinDepth", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)],
            argnames = ["a2QMarix", "iRows", "iCols", "dMinDepth", "dImageWidth", "iMaxDisparity", "dMinDepthCovered"] )
    #  ctypes.c_int imaqInterpolateDisparityImage2(ctypes.c_void_p imgDisparity, ctypes.c_void_p imageDest, ctypes.c_int iSamplingFrequency, ctypes.c_int iOrder, ctypes.c_int iMinDisp, ctypes.c_int iNumDisparities, ctypes.c_float fInvalidPixelValue, ctypes.c_int iProcessBandVal)
    addfunc(lib, "imaqInterpolateDisparityImage2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_int],
            argnames = ["imgDisparity", "imageDest", "iSamplingFrequency", "iOrder", "iMinDisp", "iNumDisparities", "fInvalidPixelValue", "iProcessBandVal"] )
    #  ctypes.c_int imaqBayerToRGB(ctypes.c_void_p srcImage, ctypes.c_void_p dstImage, ctypes.c_int bayerPattern, ctypes.c_int algorithm, ctypes.c_double blueGain, ctypes.c_double greenGain, ctypes.c_double redGain)
    addfunc(lib, "imaqBayerToRGB", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double],
            argnames = ["srcImage", "dstImage", "bayerPattern", "algorithm", "blueGain", "greenGain", "redGain"] )
    #  ctypes.c_int imaqCompareGoldenTemplate(ctypes.c_void_p image, ctypes.c_void_p goldenTemplate, ctypes.c_void_p brightDefects, ctypes.c_void_p darkDefects, ctypes.POINTER(InspectionAlignment) alignment, ctypes.POINTER(InspectionOptions) options)
    addfunc(lib, "imaqCompareGoldenTemplate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(InspectionAlignment), ctypes.POINTER(InspectionOptions)],
            argnames = ["image", "goldenTemplate", "brightDefects", "darkDefects", "alignment", "options"] )
    #  ctypes.c_int imaqLearnGoldenTemplate(ctypes.c_void_p goldenTemplate, PointFloat originOffset, ctypes.c_void_p mask)
    addfunc(lib, "imaqLearnGoldenTemplate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, PointFloat, ctypes.c_void_p],
            argnames = ["goldenTemplate", "originOffset", "mask"] )
    #  ctypes.POINTER(DetectorReport) imaqFastDetection(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_uint minFeaturePointStrength, ctypes.c_uint suppressWeakPoints)
    addfunc(lib, "imaqFastDetection", restype = ctypes.POINTER(DetectorReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint],
            argnames = ["image", "roi", "minFeaturePointStrength", "suppressWeakPoints"] )
    #  ctypes.POINTER(DetectorReport) imaqCornerDetection(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CornerOption) option, ctypes.c_uint pyramidLevel)
    addfunc(lib, "imaqCornerDetection", restype = ctypes.POINTER(DetectorReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CornerOption), ctypes.c_uint],
            argnames = ["image", "roi", "option", "pyramidLevel"] )
    #  ctypes.POINTER(DescriptorReport) imaqFeatureDescription(ctypes.c_void_p image, ctypes.POINTER(PointFloat) featurePoints, ctypes.c_uint numFeatures, ctypes.c_int method)
    addfunc(lib, "imaqFeatureDescription", restype = ctypes.POINTER(DescriptorReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(PointFloat), ctypes.c_uint, ctypes.c_int],
            argnames = ["image", "featurePoints", "numFeatures", "method"] )
    #  ctypes.POINTER(FeatureMatchingReport) imaqFeatureMatching(ctypes.POINTER(DescriptorReport) report1, ctypes.POINTER(DescriptorReport) report2, ctypes.c_double maxAcceptableDistance, ctypes.c_double errorThreshold)
    addfunc(lib, "imaqFeatureMatching", restype = ctypes.POINTER(FeatureMatchingReport),
            argtypes = [ctypes.POINTER(DescriptorReport), ctypes.POINTER(DescriptorReport), ctypes.c_double, ctypes.c_double],
            argnames = ["report1", "report2", "maxAcceptableDistance", "errorThreshold"] )
    #  ctypes.POINTER(ExtractorReport) imaqFeatureExtraction(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_uint binSize, ctypes.c_uint gridSizeX, ctypes.c_uint gridSizeY, ctypes.c_int method)
    addfunc(lib, "imaqFeatureExtraction", restype = ctypes.POINTER(ExtractorReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_int],
            argnames = ["image", "roi", "binSize", "gridSizeX", "gridSizeY", "method"] )
    #  ctypes.c_int imaqFlatFieldCorrection(ctypes.c_void_p image, ctypes.c_void_p dest, ctypes.c_void_p flatFieldImage, ctypes.c_void_p darkFieldImage, ctypes.c_void_p roi, ctypes.POINTER(FlatFieldCorrectionOptions) correctionOptions)
    addfunc(lib, "imaqFlatFieldCorrection", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(FlatFieldCorrectionOptions)],
            argnames = ["image", "dest", "flatFieldImage", "darkFieldImage", "roi", "correctionOptions"] )
    #  ctypes.c_int imaqEstimateFlatFieldModel(ctypes.c_void_p image, ctypes.c_void_p dest, ctypes.c_void_p maskImage, ctypes.c_void_p roi, ctypes.POINTER(SurfaceFitOptions) surfaceFitParams, ctypes.POINTER(BackgroundEstimation) bgEstimateParams)
    addfunc(lib, "imaqEstimateFlatFieldModel", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(SurfaceFitOptions), ctypes.POINTER(BackgroundEstimation)],
            argnames = ["image", "dest", "maskImage", "roi", "surfaceFitParams", "bgEstimateParams"] )
    #  ctypes.c_int imaqComputeAverageImage(ctypes.POINTER(ctypes.c_void_p) images, ctypes.c_uint numOfImages, ctypes.c_void_p dest)
    addfunc(lib, "imaqComputeAverageImage", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint, ctypes.c_void_p],
            argnames = ["images", "numOfImages", "dest"] )
    #  ctypes.c_int imaqComputeMedianImage(ctypes.POINTER(ctypes.c_void_p) images, ctypes.c_uint numOfImages, ctypes.c_void_p dest)
    addfunc(lib, "imaqComputeMedianImage", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_void_p), ctypes.c_uint, ctypes.c_void_p],
            argnames = ["images", "numOfImages", "dest"] )
    #  ctypes.c_int imaqOpticalFlowLucasKanade(ctypes.c_void_p currentImage, ctypes.c_void_p previousImage, ctypes.c_void_p roi, ctypes.c_void_p velocityXImage, ctypes.c_void_p velocityYImage, ctypes.POINTER(RectSize) sizeWindow, ctypes.c_int velocityRep)
    addfunc(lib, "imaqOpticalFlowLucasKanade", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(RectSize), ctypes.c_int],
            argnames = ["currentImage", "previousImage", "roi", "velocityXImage", "velocityYImage", "sizeWindow", "velocityRep"] )
    #  ctypes.c_int imaqOpticalFlowHornSchunck(ctypes.c_void_p currentImage, ctypes.c_void_p previousImage, ctypes.c_void_p roi, ctypes.c_void_p velocityXImage, ctypes.c_void_p velocityYImage, ctypes.c_int usePrevious, ctypes.c_float SmoothingParameter, ctypes.POINTER(StoppingCriteria) stopCriteria, ctypes.c_int velocityRep)
    addfunc(lib, "imaqOpticalFlowHornSchunck", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.POINTER(StoppingCriteria), ctypes.c_int],
            argnames = ["currentImage", "previousImage", "roi", "velocityXImage", "velocityYImage", "usePrevious", "SmoothingParameter", "stopCriteria", "velocityRep"] )
    #  ctypes.c_int imaqOpticalFlowPyramidLucasKanade(ctypes.c_void_p currentImage, ctypes.c_void_p previousImage, ctypes.POINTER(LKPyramidOptions) options, ctypes.POINTER(ctypes.c_float) kernel, ctypes.c_uint kernelSize, ctypes.POINTER(DifferenceArray) diffArray, ctypes.POINTER(FeaturePoints) featurePointsIn, ctypes.POINTER(FeaturePoints) featurePointsOut)
    addfunc(lib, "imaqOpticalFlowPyramidLucasKanade", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(LKPyramidOptions), ctypes.POINTER(ctypes.c_float), ctypes.c_uint, ctypes.POINTER(DifferenceArray), ctypes.POINTER(FeaturePoints), ctypes.POINTER(FeaturePoints)],
            argnames = ["currentImage", "previousImage", "options", "kernel", "kernelSize", "diffArray", "featurePointsIn", "featurePointsOut"] )
    #  ctypes.c_void_p imaqObjectTrackingCreateSession()
    addfunc(lib, "imaqObjectTrackingCreateSession", restype = ctypes.c_void_p,
            argtypes = [],
            argnames = [] )
    #  ctypes.c_int imaqObjectTrackingCloseSession(ctypes.c_void_p objectTrackingSession)
    addfunc(lib, "imaqObjectTrackingCloseSession", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p],
            argnames = ["objectTrackingSession"] )
    #  ctypes.c_int imaqObjectTrackingGetSessionInfo(ctypes.c_void_p objectTrackingSession, ctypes.POINTER(ctypes.c_int) sessionType, ctypes.POINTER(ctypes.c_int) numInstances)
    addfunc(lib, "imaqObjectTrackingGetSessionInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["objectTrackingSession", "sessionType", "numInstances"] )
    #  ctypes.c_int imaqObjectTrackingWriteSessionInfoToFile(ctypes.c_void_p objectTrackingSession, ctypes.c_char_p filename, ctypes.c_char_p description)
    addfunc(lib, "imaqObjectTrackingWriteSessionInfoToFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_char_p],
            argnames = ["objectTrackingSession", "filename", "description"] )
    #  ctypes.c_int imaqObjectTrackingReadSessionInfoFromFile(ctypes.c_void_p objectTrackingSession, ctypes.c_char_p filename, ctypes.POINTER(ctypes.c_char_p) description, ctypes.POINTER(ctypes.c_uint) _descriptionLength, ctypes.POINTER(ctypes.c_int) sessionType, ctypes.POINTER(ctypes.c_int) numObjects)
    addfunc(lib, "imaqObjectTrackingReadSessionInfoFromFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["objectTrackingSession", "filename", "description", "_descriptionLength", "sessionType", "numObjects"] )
    #  ctypes.c_int imaqObjectTrackingAddObject(ctypes.c_void_p objectTrackingSession, ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_char_p label)
    addfunc(lib, "imaqObjectTrackingAddObject", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["objectTrackingSession", "image", "roi", "label"] )
    #  ctypes.c_int imaqObjectTrackingDeleteObject(ctypes.c_void_p objectTrackingSession, ctypes.c_int instanceNumber)
    addfunc(lib, "imaqObjectTrackingDeleteObject", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["objectTrackingSession", "instanceNumber"] )
    #  ctypes.POINTER(ObjectTrackingReport) imaqObjectTrackingTrackObjects(ctypes.c_void_p objectTrackingSession, ctypes.c_void_p image, ctypes.c_int minScore)
    addfunc(lib, "imaqObjectTrackingTrackObjects", restype = ctypes.POINTER(ObjectTrackingReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["objectTrackingSession", "image", "minScore"] )
    #  ctypes.c_int imaqObjectTrackingGetObjectInfo(ctypes.c_void_p objectTrackingSession, ctypes.c_int index, ctypes.c_void_p image, ctypes.POINTER(ctypes.c_char_p) instanceLabel, ctypes.POINTER(PointDouble) location, ctypes.POINTER(ctypes.c_double) angle)
    addfunc(lib, "imaqObjectTrackingGetObjectInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_char_p), ctypes.POINTER(PointDouble), ctypes.POINTER(ctypes.c_double)],
            argnames = ["objectTrackingSession", "index", "image", "instanceLabel", "location", "angle"] )
    #  ctypes.c_int imaqObjectTrackingRenameObjectLabel(ctypes.c_void_p objectTrackingSession, ctypes.c_int index, ctypes.c_char_p instanceLabel)
    addfunc(lib, "imaqObjectTrackingRenameObjectLabel", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p],
            argnames = ["objectTrackingSession", "index", "instanceLabel"] )
    #  ctypes.c_int imaqObjectTrackingSetInitialObjectPosition(ctypes.c_void_p objectTrackingSession, ctypes.c_int index, ctypes.c_double positionX, ctypes.c_double positionY, ctypes.c_double initialAngle)
    addfunc(lib, "imaqObjectTrackingSetInitialObjectPosition", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double],
            argnames = ["objectTrackingSession", "index", "positionX", "positionY", "initialAngle"] )
    #  ctypes.c_int imaqObjectTrackingMeanShiftOptions(ctypes.c_void_p objectTrackingSession, ctypes.c_int getSetOptions, ctypes.POINTER(ctypes.c_int) numHistogramBins, ctypes.POINTER(ctypes.c_double) blendingParameter, ctypes.POINTER(ctypes.c_int) maximumIterations)
    addfunc(lib, "imaqObjectTrackingMeanShiftOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int)],
            argnames = ["objectTrackingSession", "getSetOptions", "numHistogramBins", "blendingParameter", "maximumIterations"] )
    #  ctypes.c_int imaqObjectTrackingEMeanShiftOptions(ctypes.c_void_p objectTrackingSession, ctypes.c_int getSetOptions, ctypes.POINTER(ctypes.c_int) numHistogramBins, ctypes.POINTER(ctypes.c_double) blendingParameter, ctypes.POINTER(ctypes.c_int) maximumIterations, ctypes.POINTER(ctypes.c_double) maxScaleChange, ctypes.POINTER(ctypes.c_double) maxRotationChange, ctypes.POINTER(ctypes.c_double) maxShapeChange)
    addfunc(lib, "imaqObjectTrackingEMeanShiftOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)],
            argnames = ["objectTrackingSession", "getSetOptions", "numHistogramBins", "blendingParameter", "maximumIterations", "maxScaleChange", "maxRotationChange", "maxShapeChange"] )
    #  ctypes.POINTER(ImageToStringConversionReport) imaqWriteBMPString(ctypes.c_void_p image, ctypes.c_int compress, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteBMPString", restype = ctypes.POINTER(ImageToStringConversionReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(RGBValue)],
            argnames = ["image", "compress", "colorTable"] )
    #  ctypes.POINTER(ImageToStringConversionReport) imaqWriteJPEGString(ctypes.c_void_p image, ctypes.c_uint quality, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteJPEGString", restype = ctypes.POINTER(ImageToStringConversionReport),
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.POINTER(RGBValue)],
            argnames = ["image", "quality", "colorTable"] )
    #  ctypes.POINTER(ImageToStringConversionReport) imaqWritePNGString(ctypes.c_void_p image, ctypes.c_uint quality, ctypes.c_int useBitDepth, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWritePNGString", restype = ctypes.POINTER(ImageToStringConversionReport),
            argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_int, ctypes.POINTER(RGBValue)],
            argnames = ["image", "quality", "useBitDepth", "colorTable"] )
    #  ctypes.POINTER(ImageToStringConversionReport) imaqWriteTIFFString(ctypes.c_void_p image, ctypes.POINTER(TIFFFileOptions) options, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteTIFFString", restype = ctypes.POINTER(ImageToStringConversionReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(TIFFFileOptions), ctypes.POINTER(RGBValue)],
            argnames = ["image", "options", "colorTable"] )
    #  ctypes.POINTER(ImageToStringConversionReport) imaqWriteImageAndVisionInfoString(ctypes.c_void_p image, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWriteImageAndVisionInfoString", restype = ctypes.POINTER(ImageToStringConversionReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(RGBValue)],
            argnames = ["image", "colorTable"] )
    #  ctypes.c_int imaqRotate(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_float angle, ctypes.c_int fill, ctypes.c_int method)
    addfunc(lib, "imaqRotate", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "angle", "fill", "method"] )
    #  ctypes.c_int imaqWritePNGFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.c_uint compressionSpeed, ctypes.POINTER(RGBValue) colorTable)
    addfunc(lib, "imaqWritePNGFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint, ctypes.POINTER(RGBValue)],
            argnames = ["image", "fileName", "compressionSpeed", "colorTable"] )
    #  ctypes.POINTER(ParticleReport) imaqSelectParticles(ctypes.c_void_p image, ctypes.POINTER(ParticleReport) reports, ctypes.c_int reportCount, ctypes.c_int rejectBorder, ctypes.POINTER(SelectParticleCriteria) criteria, ctypes.c_int criteriaCount, ctypes.POINTER(ctypes.c_int) selectedCount)
    addfunc(lib, "imaqSelectParticles", restype = ctypes.POINTER(ParticleReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ParticleReport), ctypes.c_int, ctypes.c_int, ctypes.POINTER(SelectParticleCriteria), ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "reports", "reportCount", "rejectBorder", "criteria", "criteriaCount", "selectedCount"] )
    #  ctypes.c_int imaqParticleFilter(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ParticleFilterCriteria) criteria, ctypes.c_int criteriaCount, ctypes.c_int rejectMatches, ctypes.c_int connectivity8)
    addfunc(lib, "imaqParticleFilter", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ParticleFilterCriteria), ctypes.c_int, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "criteria", "criteriaCount", "rejectMatches", "connectivity8"] )
    #  ctypes.POINTER(ParticleReport) imaqGetParticleInfo(ctypes.c_void_p image, ctypes.c_int connectivity8, ctypes.c_int mode, ctypes.POINTER(ctypes.c_int) reportCount)
    addfunc(lib, "imaqGetParticleInfo", restype = ctypes.POINTER(ParticleReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "connectivity8", "mode", "reportCount"] )
    #  ctypes.c_int imaqCalcCoeff(ctypes.c_void_p image, ctypes.POINTER(ParticleReport) report, ctypes.c_int parameter, ctypes.POINTER(ctypes.c_float) coefficient)
    addfunc(lib, "imaqCalcCoeff", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ParticleReport), ctypes.c_int, ctypes.POINTER(ctypes.c_float)],
            argnames = ["image", "report", "parameter", "coefficient"] )
    #  ctypes.POINTER(EdgeReport) imaqEdgeTool(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.POINTER(EdgeOptions) options, ctypes.POINTER(ctypes.c_int) numEdges)
    addfunc(lib, "imaqEdgeTool", restype = ctypes.POINTER(EdgeReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(EdgeOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "points", "numPoints", "options", "numEdges"] )
    #  ctypes.POINTER(CircleReport) imaqCircles(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_float minRadius, ctypes.c_float maxRadius, ctypes.POINTER(ctypes.c_int) numCircles)
    addfunc(lib, "imaqCircles", restype = ctypes.POINTER(CircleReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_float, ctypes.c_float, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "minRadius", "maxRadius", "numCircles"] )
    #  ctypes.c_int imaqLabel(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int connectivity8, ctypes.POINTER(ctypes.c_int) particleCount)
    addfunc(lib, "imaqLabel", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "connectivity8", "particleCount"] )
    #  ctypes.c_int imaqFitEllipse(ctypes.POINTER(PointFloat) points, ctypes.c_int numPoints, ctypes.POINTER(BestEllipse) ellipse)
    addfunc(lib, "imaqFitEllipse", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.POINTER(BestEllipse)],
            argnames = ["points", "numPoints", "ellipse"] )
    #  ctypes.c_int imaqFitCircle(ctypes.POINTER(PointFloat) points, ctypes.c_int numPoints, ctypes.POINTER(BestCircle) circle)
    addfunc(lib, "imaqFitCircle", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.POINTER(BestCircle)],
            argnames = ["points", "numPoints", "circle"] )
    #  ctypes.c_int imaqChangeColorSpace(ctypes.POINTER(ctypes.c_int) sourceColor, ctypes.c_int sourceSpace, ctypes.c_int destSpace)
    addfunc(lib, "imaqChangeColorSpace", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_int],
            argnames = ["sourceColor", "sourceSpace", "destSpace"] )
    #  ctypes.POINTER(PatternMatch) imaqMatchPattern(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(MatchPatternOptions) options, Rect searchRect, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchPattern", restype = ctypes.POINTER(PatternMatch),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(MatchPatternOptions), Rect, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "options", "searchRect", "numMatches"] )
    #  ctypes.c_int imaqConvex(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqConvex", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqIsVisionInfoPresent(ctypes.c_void_p image, ctypes.c_int type, ctypes.POINTER(ctypes.c_int) present)
    addfunc(lib, "imaqIsVisionInfoPresent", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "type", "present"] )
    #  ctypes.c_int imaqLineGaugeTool(ctypes.c_void_p image, Point start, Point end, ctypes.c_int method, ctypes.POINTER(EdgeOptions) edgeOptions, ctypes.POINTER(CoordinateTransform) reference, ctypes.POINTER(ctypes.c_float) distance)
    addfunc(lib, "imaqLineGaugeTool", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, Point, ctypes.c_int, ctypes.POINTER(EdgeOptions), ctypes.POINTER(CoordinateTransform), ctypes.POINTER(ctypes.c_float)],
            argnames = ["image", "start", "end", "method", "edgeOptions", "reference", "distance"] )
    #  ctypes.c_int imaqBestCircle(ctypes.POINTER(PointFloat) points, ctypes.c_int numPoints, ctypes.POINTER(PointFloat) center, ctypes.POINTER(ctypes.c_double) radius)
    addfunc(lib, "imaqBestCircle", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(PointFloat), ctypes.c_int, ctypes.POINTER(PointFloat), ctypes.POINTER(ctypes.c_double)],
            argnames = ["points", "numPoints", "center", "radius"] )
    #  ctypes.c_int imaqSavePattern(ctypes.c_void_p pattern, ctypes.c_char_p fileName)
    addfunc(lib, "imaqSavePattern", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["pattern", "fileName"] )
    #  ctypes.c_int imaqLoadPattern(ctypes.c_void_p pattern, ctypes.c_char_p fileName)
    addfunc(lib, "imaqLoadPattern", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p],
            argnames = ["pattern", "fileName"] )
    #  ctypes.c_int imaqTransformROI(ctypes.c_void_p roi, Point originStart, ctypes.c_float angleStart, Point originFinal, ctypes.c_float angleFinal)
    addfunc(lib, "imaqTransformROI", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, Point, ctypes.c_float, Point, ctypes.c_float],
            argnames = ["roi", "originStart", "angleStart", "originFinal", "angleFinal"] )
    #  ctypes.c_int imaqCoordinateReference(ctypes.POINTER(Point) points, ctypes.c_int mode, ctypes.POINTER(Point) origin, ctypes.POINTER(ctypes.c_float) angle)
    addfunc(lib, "imaqCoordinateReference", restype = ctypes.c_int,
            argtypes = [ctypes.POINTER(Point), ctypes.c_int, ctypes.POINTER(Point), ctypes.POINTER(ctypes.c_float)],
            argnames = ["points", "mode", "origin", "angle"] )
    #  ctypes.POINTER(ContourInfo) imaqGetContourInfo(ctypes.c_void_p roi, ContourID id)
    addfunc(lib, "imaqGetContourInfo", restype = ctypes.POINTER(ContourInfo),
            argtypes = [ctypes.c_void_p, ContourID],
            argnames = ["roi", "id"] )
    #  ctypes.c_int imaqSetWindowOverlay(ctypes.c_int windowNumber, ctypes.c_void_p overlay)
    addfunc(lib, "imaqSetWindowOverlay", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_void_p],
            argnames = ["windowNumber", "overlay"] )
    #  ctypes.c_void_p imaqCreateOverlayFromROI(ctypes.c_void_p roi)
    addfunc(lib, "imaqCreateOverlayFromROI", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p],
            argnames = ["roi"] )
    #  ctypes.c_void_p imaqCreateOverlayFromMetafile(ctypes.c_void_p metafile)
    addfunc(lib, "imaqCreateOverlayFromMetafile", restype = ctypes.c_void_p,
            argtypes = [ctypes.c_void_p],
            argnames = ["metafile"] )
    #  ctypes.c_int imaqSetCalibrationInfo(ctypes.c_void_p image, ctypes.c_int unit, ctypes.c_float xDistance, ctypes.c_float yDistance)
    addfunc(lib, "imaqSetCalibrationInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_float],
            argnames = ["image", "unit", "xDistance", "yDistance"] )
    #  ctypes.c_int imaqGetCalibrationInfo(ctypes.c_void_p image, ctypes.POINTER(ctypes.c_int) unit, ctypes.POINTER(ctypes.c_float) xDistance, ctypes.POINTER(ctypes.c_float) yDistance)
    addfunc(lib, "imaqGetCalibrationInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float)],
            argnames = ["image", "unit", "xDistance", "yDistance"] )
    #  ctypes.c_int imaqConstructROI(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int initialTool, ctypes.POINTER(ToolWindowOptions) tools, ctypes.POINTER(ConstructROIOptions) options, ctypes.POINTER(ctypes.c_int) okay)
    addfunc(lib, "imaqConstructROI", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ToolWindowOptions), ctypes.POINTER(ConstructROIOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "roi", "initialTool", "tools", "options", "okay"] )
    #  ctypes.POINTER(SpokeReport) imaqSpoke(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.POINTER(SpokeOptions) options)
    addfunc(lib, "imaqSpoke", restype = ctypes.POINTER(SpokeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(SpokeOptions)],
            argnames = ["image", "roi", "direction", "process", "options"] )
    #  ctypes.c_int imaqLookup(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ctypes.c_short) table, ctypes.c_void_p mask)
    addfunc(lib, "imaqLookup", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_short), ctypes.c_void_p],
            argnames = ["dest", "source", "table", "mask"] )
    #  ctypes.c_int imaqGetParticleClassifierOptions(ctypes.c_void_p session, ctypes.POINTER(ParticleClassifierPreprocessingOptions) preprocessingOptions, ctypes.POINTER(ParticleClassifierOptions) options)
    addfunc(lib, "imaqGetParticleClassifierOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ParticleClassifierPreprocessingOptions), ctypes.POINTER(ParticleClassifierOptions)],
            argnames = ["session", "preprocessingOptions", "options"] )
    #  ctypes.c_int imaqSetParticleClassifierOptions(ctypes.c_void_p session, ctypes.POINTER(ParticleClassifierPreprocessingOptions) preprocessingOptions, ctypes.POINTER(ParticleClassifierOptions) options)
    addfunc(lib, "imaqSetParticleClassifierOptions", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(ParticleClassifierPreprocessingOptions), ctypes.POINTER(ParticleClassifierOptions)],
            argnames = ["session", "preprocessingOptions", "options"] )
    #  ctypes.c_int imaqZoomWindow(ctypes.c_int windowNumber, ctypes.c_int xZoom, ctypes.c_int yZoom, Point center)
    addfunc(lib, "imaqZoomWindow", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, Point],
            argnames = ["windowNumber", "xZoom", "yZoom", "center"] )
    #  ctypes.c_int imaqGetWindowZoom(ctypes.c_int windowNumber, ctypes.POINTER(ctypes.c_int) xZoom, ctypes.POINTER(ctypes.c_int) yZoom)
    addfunc(lib, "imaqGetWindowZoom", restype = ctypes.c_int,
            argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)],
            argnames = ["windowNumber", "xZoom", "yZoom"] )
    #  ctypes.c_int imaqParticleFilter3(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ParticleFilterCriteria2) criteria, ctypes.c_int criteriaCount, ctypes.POINTER(ParticleFilterOptions) options, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numParticles)
    addfunc(lib, "imaqParticleFilter3", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ParticleFilterCriteria2), ctypes.c_int, ctypes.POINTER(ParticleFilterOptions), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "criteria", "criteriaCount", "options", "roi", "numParticles"] )
    #  ctypes.POINTER(ReadTextReport2) imaqReadText2(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.c_void_p roi, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions) processingOptions, ctypes.POINTER(OCRSpacingOptions) spacingOptions)
    addfunc(lib, "imaqReadText2", restype = ctypes.POINTER(ReadTextReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions), ctypes.POINTER(OCRSpacingOptions)],
            argnames = ["image", "set", "roi", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.POINTER(ReadTextReport3) imaqReadText3(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.c_void_p roi, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions) processingOptions, ctypes.POINTER(OCRSpacingOptions) spacingOptions)
    addfunc(lib, "imaqReadText3", restype = ctypes.POINTER(ReadTextReport3),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions), ctypes.POINTER(OCRSpacingOptions)],
            argnames = ["image", "set", "roi", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.c_int imaqTrainChars(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.c_int index, ctypes.c_char_p charValue, ctypes.c_void_p roi, ctypes.POINTER(OCRProcessingOptions) processingOptions, ctypes.POINTER(OCRSpacingOptions) spacingOptions)
    addfunc(lib, "imaqTrainChars", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p, ctypes.POINTER(OCRProcessingOptions), ctypes.POINTER(OCRSpacingOptions)],
            argnames = ["image", "set", "index", "charValue", "roi", "processingOptions", "spacingOptions"] )
    #  ctypes.c_int imaqReadOCRFile(ctypes.c_char_p fileName, ctypes.c_void_p set, String255 setDescription, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions) processingOptions, ctypes.POINTER(OCRSpacingOptions) spacingOptions)
    addfunc(lib, "imaqReadOCRFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_void_p, String255, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions), ctypes.POINTER(OCRSpacingOptions)],
            argnames = ["fileName", "set", "setDescription", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.c_int imaqWriteOCRFile(ctypes.c_char_p fileName, ctypes.c_void_p set, ctypes.c_char_p setDescription, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions) processingOptions, ctypes.POINTER(OCRSpacingOptions) spacingOptions)
    addfunc(lib, "imaqWriteOCRFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_char_p, ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions), ctypes.POINTER(OCRSpacingOptions)],
            argnames = ["fileName", "set", "setDescription", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.c_int imaqLearnPattern2(ctypes.c_void_p image, ctypes.c_int learningMode, ctypes.POINTER(LearnPatternAdvancedOptions) advancedOptions)
    addfunc(lib, "imaqLearnPattern2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(LearnPatternAdvancedOptions)],
            argnames = ["image", "learningMode", "advancedOptions"] )
    #  ctypes.c_int imaqConvolve(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ctypes.c_float) kernel, ctypes.c_int matrixRows, ctypes.c_int matrixCols, ctypes.c_float normalize, ctypes.c_void_p mask)
    addfunc(lib, "imaqConvolve", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int, ctypes.c_float, ctypes.c_void_p],
            argnames = ["dest", "source", "kernel", "matrixRows", "matrixCols", "normalize", "mask"] )
    #  ctypes.c_int imaqDivideConstant(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int value)
    addfunc(lib, "imaqDivideConstant", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int],
            argnames = ["dest", "source", "value"] )
    #  ctypes.c_int imaqDivide(ctypes.c_void_p dest, ctypes.c_void_p sourceA, ctypes.c_void_p sourceB)
    addfunc(lib, "imaqDivide", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "sourceA", "sourceB"] )
    #  ctypes.c_int imaqLearnPattern(ctypes.c_void_p image, ctypes.c_int learningMode)
    addfunc(lib, "imaqLearnPattern", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["image", "learningMode"] )
    #  ctypes.POINTER(ConcentricRakeReport) imaqConcentricRake(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.POINTER(RakeOptions) options)
    addfunc(lib, "imaqConcentricRake", restype = ctypes.POINTER(ConcentricRakeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(RakeOptions)],
            argnames = ["image", "roi", "direction", "process", "options"] )
    #  ctypes.POINTER(PatternMatch) imaqMatchPattern2(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(MatchPatternOptions) options, ctypes.POINTER(MatchPatternAdvancedOptions) advancedOptions, Rect searchRect, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchPattern2", restype = ctypes.POINTER(PatternMatch),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(MatchPatternOptions), ctypes.POINTER(MatchPatternAdvancedOptions), Rect, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "options", "advancedOptions", "searchRect", "numMatches"] )
    #  ctypes.POINTER(RakeReport) imaqRake(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.POINTER(RakeOptions) options)
    addfunc(lib, "imaqRake", restype = ctypes.POINTER(RakeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(RakeOptions)],
            argnames = ["image", "roi", "direction", "process", "options"] )
    #  ctypes.c_int imaqCopyCalibrationInfo(ctypes.c_void_p dest, ctypes.c_void_p source)
    addfunc(lib, "imaqCopyCalibrationInfo", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["dest", "source"] )
    #  ctypes.c_int imaqParticleFilter2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.POINTER(ParticleFilterCriteria2) criteria, ctypes.c_int criteriaCount, ctypes.c_int rejectMatches, ctypes.c_int connectivity8, ctypes.POINTER(ctypes.c_int) numParticles)
    addfunc(lib, "imaqParticleFilter2", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ParticleFilterCriteria2), ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "criteria", "criteriaCount", "rejectMatches", "connectivity8", "numParticles"] )
    #  ctypes.POINTER(EdgeReport) imaqEdgeTool2(ctypes.c_void_p image, ctypes.POINTER(Point) points, ctypes.c_int numPoints, ctypes.c_int process, ctypes.POINTER(EdgeOptions) options, ctypes.POINTER(ctypes.c_int) numEdges)
    addfunc(lib, "imaqEdgeTool2", restype = ctypes.POINTER(EdgeReport),
            argtypes = [ctypes.c_void_p, ctypes.POINTER(Point), ctypes.c_int, ctypes.c_int, ctypes.POINTER(EdgeOptions), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "points", "numPoints", "process", "options", "numEdges"] )
    #  ContourID imaqAddRotatedRectContour(ctypes.c_void_p roi, RotatedRect rect)
    addfunc(lib, "imaqAddRotatedRectContour", restype = ContourID,
            argtypes = [ctypes.c_void_p, RotatedRect],
            argnames = ["roi", "rect"] )
    #  ctypes.POINTER(Barcode2DInfo) imaqReadDataMatrixBarcode(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(DataMatrixOptions) options, ctypes.POINTER(ctypes.c_uint) numBarcodes)
    addfunc(lib, "imaqReadDataMatrixBarcode", restype = ctypes.POINTER(Barcode2DInfo),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(DataMatrixOptions), ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "roi", "options", "numBarcodes"] )
    #  ctypes.POINTER(LinearAverages) imaqLinearAverages(ctypes.c_void_p image, Rect rect)
    addfunc(lib, "imaqLinearAverages", restype = ctypes.POINTER(LinearAverages),
            argtypes = [ctypes.c_void_p, Rect],
            argnames = ["image", "rect"] )
    #  ctypes.POINTER(GeometricPatternMatch) imaqMatchGeometricPattern(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(MatchGeometricPatternOptions) matchOptions, ctypes.POINTER(MatchGeometricPatternAdvancedOptions) advancedMatchOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchGeometricPattern", restype = ctypes.POINTER(GeometricPatternMatch),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CurveOptions), ctypes.POINTER(MatchGeometricPatternOptions), ctypes.POINTER(MatchGeometricPatternAdvancedOptions), ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "pattern", "curveOptions", "matchOptions", "advancedMatchOptions", "roi", "numMatches"] )
    #  ctypes.POINTER(GeometricPatternMatch3) imaqMatchGeometricPattern3(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(MatchGeometricPatternOptions) matchOptions, ctypes.POINTER(MatchGeometricPatternAdvancedOptions3) advancedMatchOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_size_t) numMatches)
    addfunc(lib, "imaqMatchGeometricPattern3", restype = ctypes.POINTER(GeometricPatternMatch3),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CurveOptions), ctypes.POINTER(MatchGeometricPatternOptions), ctypes.POINTER(MatchGeometricPatternAdvancedOptions3), ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["image", "pattern", "curveOptions", "matchOptions", "advancedMatchOptions", "roi", "numMatches"] )
    #  ctypes.POINTER(GeometricPatternMatch3) imaqMatchGeometricPattern4(ctypes.c_void_p image, ctypes.c_void_p pattern, ctypes.POINTER(CurveOptions) curveOptions, ctypes.POINTER(MatchGeometricPatternOptions) matchOptions, ctypes.POINTER(MatchGeometricPatternAdvancedOptions4) advancedMatchOptions, ctypes.c_void_p roi, ctypes.POINTER(ctypes.c_size_t) numMatches)
    addfunc(lib, "imaqMatchGeometricPattern4", restype = ctypes.POINTER(GeometricPatternMatch3),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CurveOptions), ctypes.POINTER(MatchGeometricPatternOptions), ctypes.POINTER(MatchGeometricPatternAdvancedOptions4), ctypes.c_void_p, ctypes.POINTER(ctypes.c_size_t)],
            argnames = ["image", "pattern", "curveOptions", "matchOptions", "advancedMatchOptions", "roi", "numMatches"] )
    #  ctypes.POINTER(CharInfo) imaqGetCharInfo(ctypes.c_void_p set, ctypes.c_int index)
    addfunc(lib, "imaqGetCharInfo", restype = ctypes.POINTER(CharInfo),
            argtypes = [ctypes.c_void_p, ctypes.c_int],
            argnames = ["set", "index"] )
    #  ctypes.POINTER(ReadTextReport) imaqReadText(ctypes.c_void_p image, ctypes.c_void_p set, ctypes.c_void_p roi, ctypes.POINTER(ReadTextOptions) readOptions, ctypes.POINTER(OCRProcessingOptions) processingOptions, ctypes.POINTER(OCRSpacingOptions) spacingOptions)
    addfunc(lib, "imaqReadText", restype = ctypes.POINTER(ReadTextReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(ReadTextOptions), ctypes.POINTER(OCRProcessingOptions), ctypes.POINTER(OCRSpacingOptions)],
            argnames = ["image", "set", "roi", "readOptions", "processingOptions", "spacingOptions"] )
    #  ctypes.POINTER(ThresholdData) imaqAutoThreshold(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int numClasses, ctypes.c_int method)
    addfunc(lib, "imaqAutoThreshold", restype = ctypes.POINTER(ThresholdData),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int],
            argnames = ["dest", "source", "numClasses", "method"] )
    #  ctypes.POINTER(ColorHistogramReport) imaqColorHistogram(ctypes.c_void_p image, ctypes.c_int numClasses, ctypes.c_int mode, ctypes.c_void_p mask)
    addfunc(lib, "imaqColorHistogram", restype = ctypes.POINTER(ColorHistogramReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p],
            argnames = ["image", "numClasses", "mode", "mask"] )
    #  ctypes.POINTER(EdgeReport2) imaqEdgeTool3(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int processType, ctypes.POINTER(EdgeOptions2) edgeOptions)
    addfunc(lib, "imaqEdgeTool3", restype = ctypes.POINTER(EdgeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(EdgeOptions2)],
            argnames = ["image", "roi", "processType", "edgeOptions"] )
    #  ctypes.POINTER(ClampMax2Report) imaqClampMax2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(CoordinateSystem) baseSystem, ctypes.POINTER(CoordinateSystem) newSystem, ctypes.POINTER(CurveOptions) curveSettings, ctypes.POINTER(ClampSettings) clampSettings, ctypes.POINTER(ClampOverlaySettings) clampOverlaySettings)
    addfunc(lib, "imaqClampMax2", restype = ctypes.POINTER(ClampMax2Report),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CoordinateSystem), ctypes.POINTER(CurveOptions), ctypes.POINTER(ClampSettings), ctypes.POINTER(ClampOverlaySettings)],
            argnames = ["image", "roi", "baseSystem", "newSystem", "curveSettings", "clampSettings", "clampOverlaySettings"] )
    #  ctypes.POINTER(ColorHistogramReport) imaqColorHistogram2(ctypes.c_void_p image, ctypes.c_int numClasses, ctypes.c_int mode, ctypes.POINTER(CIEXYZValue) whiteReference, ctypes.c_void_p mask)
    addfunc(lib, "imaqColorHistogram2", restype = ctypes.POINTER(ColorHistogramReport),
            argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.POINTER(CIEXYZValue), ctypes.c_void_p],
            argnames = ["image", "numClasses", "mode", "whiteReference", "mask"] )
    #  ctypes.POINTER(ShapeReport) imaqMatchShape(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_void_p templateImage, ctypes.c_int scaleInvariant, ctypes.c_int connectivity8, ctypes.c_double tolerance, ctypes.POINTER(ctypes.c_int) numMatches)
    addfunc(lib, "imaqMatchShape", restype = ctypes.POINTER(ShapeReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_double, ctypes.POINTER(ctypes.c_int)],
            argnames = ["dest", "source", "templateImage", "scaleInvariant", "connectivity8", "tolerance", "numMatches"] )
    #  ctypes.POINTER(QuantifyReport) imaqQuantify(ctypes.c_void_p image, ctypes.c_void_p mask)
    addfunc(lib, "imaqQuantify", restype = ctypes.POINTER(QuantifyReport),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p],
            argnames = ["image", "mask"] )
    #  ctypes.c_int imaqCalibrationCorrectionLearnSetup(ctypes.c_void_p templateImage, ctypes.POINTER(CalibrationCorrectionLearnSetupInfo) setupInfo, ctypes.c_void_p roi)
    addfunc(lib, "imaqCalibrationCorrectionLearnSetup", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.POINTER(CalibrationCorrectionLearnSetupInfo), ctypes.c_void_p],
            argnames = ["templateImage", "setupInfo", "roi"] )
    #  ctypes.c_int imaqGrayMorphology(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int method, ctypes.POINTER(StructuringElement) structuringElement)
    addfunc(lib, "imaqGrayMorphology", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(StructuringElement)],
            argnames = ["dest", "source", "method", "structuringElement"] )
    #  ctypes.POINTER(ThresholdData) imaqAutoThreshold2(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int numClasses, ctypes.c_int method, ctypes.c_void_p mask)
    addfunc(lib, "imaqAutoThreshold2", restype = ctypes.POINTER(ThresholdData),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p],
            argnames = ["dest", "source", "numClasses", "method", "mask"] )
    #  ctypes.POINTER(ConcentricRakeReport2) imaqConcentricRake2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.c_int stepSize, ctypes.POINTER(EdgeOptions2) edgeOptions)
    addfunc(lib, "imaqConcentricRake2", restype = ctypes.POINTER(ConcentricRakeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(EdgeOptions2)],
            argnames = ["image", "roi", "direction", "process", "stepSize", "edgeOptions"] )
    #  ctypes.POINTER(RakeReport2) imaqRake2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.c_int stepSize, ctypes.POINTER(EdgeOptions2) edgeOptions)
    addfunc(lib, "imaqRake2", restype = ctypes.POINTER(RakeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(EdgeOptions2)],
            argnames = ["image", "roi", "direction", "process", "stepSize", "edgeOptions"] )
    #  ctypes.POINTER(SpokeReport2) imaqSpoke2(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.c_int direction, ctypes.c_int process, ctypes.c_int stepSize, ctypes.POINTER(EdgeOptions2) edgeOptions)
    addfunc(lib, "imaqSpoke2", restype = ctypes.POINTER(SpokeReport2),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(EdgeOptions2)],
            argnames = ["image", "roi", "direction", "process", "stepSize", "edgeOptions"] )
    #  ctypes.POINTER(CalibrationReferencePoints) imaqCalibrationTargetToPoints(ctypes.c_void_p image, ctypes.c_void_p roi, ctypes.POINTER(GridDescriptor) gridDescriptor, ctypes.POINTER(MaxGridSize) maxGridSize)
    addfunc(lib, "imaqCalibrationTargetToPoints", restype = ctypes.POINTER(CalibrationReferencePoints),
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.POINTER(GridDescriptor), ctypes.POINTER(MaxGridSize)],
            argnames = ["image", "roi", "gridDescriptor", "maxGridSize"] )
    #  ctypes.c_int imaqROIToMask(ctypes.c_void_p mask, ctypes.c_void_p roi, ctypes.c_int fillValue, ctypes.c_void_p imageModel, ctypes.POINTER(ctypes.c_int) inSpace)
    addfunc(lib, "imaqROIToMask", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int)],
            argnames = ["mask", "roi", "fillValue", "imageModel", "inSpace"] )
    #  ctypes.POINTER(FilterName) imaqGetFilterNames(ctypes.POINTER(ctypes.c_int) numFilters)
    addfunc(lib, "imaqGetFilterNames", restype = ctypes.POINTER(FilterName),
            argtypes = [ctypes.POINTER(ctypes.c_int)],
            argnames = ["numFilters"] )
    #  AVISession imaqCreateAVI(ctypes.c_char_p fileName, ctypes.c_char_p compressionFilter, ctypes.c_int quality, ctypes.c_uint framesPerSecond, ctypes.c_uint maxDataSize)
    addfunc(lib, "imaqCreateAVI", restype = AVISession,
            argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint],
            argnames = ["fileName", "compressionFilter", "quality", "framesPerSecond", "maxDataSize"] )
    #  ctypes.c_int imaqWriteAVIFrame(ctypes.c_void_p image, AVISession session, ctypes.c_void_p data, ctypes.c_uint dataLength)
    addfunc(lib, "imaqWriteAVIFrame", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, AVISession, ctypes.c_void_p, ctypes.c_uint],
            argnames = ["image", "session", "data", "dataLength"] )
    #  AVISession imaqOpenAVI(ctypes.c_char_p fileName)
    addfunc(lib, "imaqOpenAVI", restype = AVISession,
            argtypes = [ctypes.c_char_p],
            argnames = ["fileName"] )
    #  ctypes.c_int imaqReadAVIFrame(ctypes.c_void_p image, AVISession session, ctypes.c_uint frameNum, ctypes.c_void_p data, ctypes.POINTER(ctypes.c_uint) dataSize)
    addfunc(lib, "imaqReadAVIFrame", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, AVISession, ctypes.c_uint, ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint)],
            argnames = ["image", "session", "frameNum", "data", "dataSize"] )
    #  ctypes.c_int imaqGetAVIInfo(AVISession session, ctypes.POINTER(AVIInfo) info)
    addfunc(lib, "imaqGetAVIInfo", restype = ctypes.c_int,
            argtypes = [AVISession, ctypes.POINTER(AVIInfo)],
            argnames = ["session", "info"] )
    #  ctypes.c_int imaqCloseAVI(AVISession session)
    addfunc(lib, "imaqCloseAVI", restype = ctypes.c_int,
            argtypes = [AVISession],
            argnames = ["session"] )
    #  ctypes.c_int imaqLocalThreshold(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_uint windowWidth, ctypes.c_uint windowHeight, ctypes.c_int method, ctypes.c_double deviationWeight, ctypes.c_int type, ctypes.c_float replaceValue)
    addfunc(lib, "imaqLocalThreshold", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_double, ctypes.c_int, ctypes.c_float],
            argnames = ["dest", "source", "windowWidth", "windowHeight", "method", "deviationWeight", "type", "replaceValue"] )
    #  ctypes.c_int imaqLearnPattern4(ctypes.c_void_p templateImage, ctypes.c_void_p maskImage, ctypes.c_int matchingAlgorithm, ctypes.POINTER(RotationAngleRange) rotationAngleRange, ctypes.POINTER(PMLearnAdvancedSetupDataOption) advancedOptionsHandle, ctypes.c_uint numAdvancedOptions, ctypes.POINTER(TemplateReport) templateReport)
    addfunc(lib, "imaqLearnPattern4", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(RotationAngleRange), ctypes.POINTER(PMLearnAdvancedSetupDataOption), ctypes.c_uint, ctypes.POINTER(TemplateReport)],
            argnames = ["templateImage", "maskImage", "matchingAlgorithm", "rotationAngleRange", "advancedOptionsHandle", "numAdvancedOptions", "templateReport"] )
    #  ctypes.c_int imaqLearnPattern5(ctypes.c_void_p templateImage, ctypes.c_void_p weightMap, ctypes.c_void_p maskImage, ctypes.c_int matchingAlgorithm, ctypes.POINTER(RotationAngleRange) rotationAngleRange, ctypes.POINTER(PMLearnAdvancedSetupDataOption) advancedOptionsHandle, ctypes.c_uint numAdvancedOptions, ctypes.POINTER(TemplateReport) templateReport)
    addfunc(lib, "imaqLearnPattern5", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(RotationAngleRange), ctypes.POINTER(PMLearnAdvancedSetupDataOption), ctypes.c_uint, ctypes.POINTER(TemplateReport)],
            argnames = ["templateImage", "weightMap", "maskImage", "matchingAlgorithm", "rotationAngleRange", "advancedOptionsHandle", "numAdvancedOptions", "templateReport"] )
    #  ctypes.c_int imaqReadFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.POINTER(RGBValue) colorTable, ctypes.POINTER(ctypes.c_int) numColors)
    addfunc(lib, "imaqReadFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(RGBValue), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "fileName", "colorTable", "numColors"] )
    #  ctypes.c_int imaqReadVisionFile(ctypes.c_void_p image, ctypes.c_char_p fileName, ctypes.POINTER(RGBValue) colorTable, ctypes.POINTER(ctypes.c_int) numColors)
    addfunc(lib, "imaqReadVisionFile", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(RGBValue), ctypes.POINTER(ctypes.c_int)],
            argnames = ["image", "fileName", "colorTable", "numColors"] )
    #  ctypes.c_int imaqCast(ctypes.c_void_p dest, ctypes.c_void_p source, ctypes.c_int type, ctypes.POINTER(ctypes.c_float) lookup, ctypes.c_int shift)
    addfunc(lib, "imaqCast", restype = ctypes.c_int,
            argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.c_int],
            argnames = ["dest", "source", "type", "lookup", "shift"] )


