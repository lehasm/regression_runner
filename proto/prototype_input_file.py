"""
Prototype input file

An example input file to manage test runs
from user point of view
"""

# Use module with environment and following functions
from regression_runner import *

# Specify log path
# (convenient default value may be used, like ./logs/${time_tag},
# for example results in ./logs/2017_08_20__13_17_08 )
#
# Add custom pattern to substitute (globally available):
# include all arguments in folder name
Substitute("log_path", "_".join(["./logs/", time_tag] + Args()))

# Environment variables may be accessed
# "or ..." is used to return default path when PROJECT_PATH is not defined
Substitute("fw_path", Env("PROJECT_PATH") or "../.." + "/fw")

# Create and initialize test group
Group(
    group_name      = "main_tests",
    count           = 5,                # specify test run count
    timeout         = 300,              # set test execution timeout (in seconds)

    # Substitution patterns may be specified even here (more clear look)
    test_log        = "${log_path}/${test_name}.${run_index}.log"
    test_fw         = "${fw_path}/${test_name}"

    # A list of commands is enclosed in '[', ']' (single command - just an ordinary string)
    test_commands   = [
                        "make -C ${test_fw}",
                        "ln -s -f -T ${test_fw}/build/ROM.memh ROM.memh",
                        "irun -f irun.f -l ${test_log} ${run_args} ${global_run_args}"
                      ],
    # Every command exit code may be accessed via CommandExitCode(n)
    # All exit codes via CommandExitCode()

    # Predefined check scripts are available
    # The following constructs check script which analyse log file (or files)
    # to find required and forbidden strings
    test_check      = CreateLogFilter(
                        "${test_log}"
                        required_string     = "TEST DONE",
                        forbidden_string    = "TEST ERROR"
                        ),
    # check_script return codes are used in summary output
    # None or empty list - successful check
    # Non empty list contains error descriptions

    # Take actions after all tests in a group have finished
    # Functions (user defined or predefined)
    # may be specified instead of raw console commands
    post_commands   = CreateReportGenerator()
)


# Add tests to recently created group
Test("fifo_test")                   # shortest form: just test name

Test(
        name        = "reset_test", # extended form:
        count       = 1             # override group properties
)

Test(
        name        = "read_memory_model_test",

        # Additional arguments will be inserted in a run script pattern
        run_args    = "+define+CONNECT_MEMORY_MODEL"
    )

# Some tests may be run conditionally
if ("NETLIST" not in Args()):
    # This file is a Python script actually
    # so valid indentation of command blocks are required
    # (invalid indentation results in IndentationError exception)
    Test("memory_full_test")

# Run regression
Run(
    # Some customization may be done for entire regression run
    pre_commands    = "echo Pojehali!",
    post_commands   = ["echo Time to relax", "shutdown"],

    parallel_processes = 2,         # parallel test execution is supported
    parallel_groups_allowed = 1     # manage parallel group execution
)
