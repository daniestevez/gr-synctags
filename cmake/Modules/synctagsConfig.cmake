INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_SYNCTAGS synctags)

FIND_PATH(
    SYNCTAGS_INCLUDE_DIRS
    NAMES synctags/api.h
    HINTS $ENV{SYNCTAGS_DIR}/include
        ${PC_SYNCTAGS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    SYNCTAGS_LIBRARIES
    NAMES gnuradio-synctags
    HINTS $ENV{SYNCTAGS_DIR}/lib
        ${PC_SYNCTAGS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(SYNCTAGS DEFAULT_MSG SYNCTAGS_LIBRARIES SYNCTAGS_INCLUDE_DIRS)
MARK_AS_ADVANCED(SYNCTAGS_LIBRARIES SYNCTAGS_INCLUDE_DIRS)

