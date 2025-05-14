import warnings

# Unfortunately, kurrentdbclient triggers a lot of UserWarnings that
# cloud the output. Since we cannot easily control that, we suppress
# warnings for the exercise_03 module.
#
# Don't use this in production code, you might miss something important!
warnings.filterwarnings("ignore")
