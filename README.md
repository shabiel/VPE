# Victory Programming Environment (VPE)
This is an updated version of VPE from the last version released by David
Bolduc. David Bolduc passed away in 2013.

The home page of VPE is http://hardhats.org/tools/vpe/vpe_db.html.

## Install
Go to the releases page, and download the latest VPE_vvPv.RSA file:

https://github.com/shabiel/VPE/releases.

Load this in with your M Implementations Routine Input utility, and then type
in Programmer Mode `D ^XV`

This command both starts VPE and installs it for the first time if it is not
already installed.

VPE does not rely on VISTA or RPMS being installed. You can use a lot of its
functionality without VISTA or RPMS. Anything Fileman-related will not work if
Fileman isn't installed.

## Upgrade
To upgrade VPE, ensure that all users are logged out of VPE, and then from
outside VPE run `DO UPGRADE^XV`.

## Uninstall
To uninstall VPE, from outside of VPE run `DO RESET^XV`, and then delete all
the XV* routines (with the exception of XVIR*, which belong to the Kernel).

## Using VPE (Brief User Manual)
To enter VPE, type `D ^XV`.  An online manual can be found by just typing '?'
when at the '>>' VPE prompt. 

VPE has its own CHUI Windowing system. To get out of any windows, type 'ESC',
'ESC'... that is, two escapes in a row. That's the only shortcut key you really
need to remember.

v15.0 introduces syntax highlighting as a feature. It is not enabled by default.
Type `..PARAM` and choose `8. Highlight Syntax....` in order to turn syntax
highlighting on. By default, syntax colors are optimized for a black background;
if you wish to change the colors, choose `9. Configure Syntax....`. Note that
the latter only apprers only if Syntax Highlighting is toggled on from option 8.
Many thanks to David Wicksell for writing the Syntax Highlighter.

The VPE manual can be found [here](docs/VPEUSER.pdf). Since the original VPE
manual has been written, VPE has been moved to XVEM from %ZVEM or ZVEM.
Therefore, any references to %ZVEM or ZVEM should be changed to XVEM.

## Unit Testing
VPE (as of version 14.2) comes with a Unit Testing suite that covers about 55%
of the code. The tests are somewhat brittle due to the reliance on specific 
strings which may change between Fileman versions, due to how much global data
is in a system, and due to issues with race conditions in PExpect. The authors
do guarantee that the tests would run on FOIA VistA on GT.M and Cache.

They To run the Unit Testing suite, do the following:

1. Make sure you have VPE imported into your M-implementation (preferably the
   routines in this repository rather than the release).
2. Clone the [OSEHRA VistA](https://github.com/OSEHRA/VistA) repository for the
   VistA testing framework.
3. Install the latest M-Unit (1.6) from https://github.com/ChristopherEdwards/M-Unit
   (importing routines only -- not installing KIDS build -- is fine)
4. Install python3 and pip3
5. Install Pexpect requirements by typing `pip install -r VistA/requirements.txt`
6. Set environment variables for your VistA instance. For GT.M, you need
   `gtmroutines`, `gtm_dist`, and `gtmgbldir`. For Caché, you need CACHE_INSTANCE
   and CACHE_NAMESPACE
7. Run the following command, modifying the PYTHONPATH to include the
   `Python/vista` path in the [OSEHRA VistA](https://github.com/OSEHRA/VistA)
   repository

```
PYTHONPATH=$PYTHONPATH:../VistA/Python/vista python3 tests/VPE_test.py -c ON -cs 'XV*,-XVIR*' /tmp/
```

This is the expected output:
```
test_deleteVPE (__main__.VPEUnitTests) ... ok
test_startVPE (__main__.VPEUnitTests) ... ok
test_startVPE_with_v12_installed (__main__.VPEUnitTests) ... ok
test_tryStartAgainFromWithin (__main__.VPEUnitTests) ... ok
test_tryDUZ999999999 (__main__.VPEUnitTests) ... ok
test_qwiks (__main__.VPEUnitTests) ... ok
test_command_line_shortcuts (__main__.VPEUnitTests) ... ok
test_command_line_error_trap (__main__.VPEUnitTests) ... ok
test_command_line_global_warn (__main__.VPEUnitTests) ... ok
test_main_help (__main__.VPEUnitTests) ... ok
test_delete_routine (__main__.VPEUnitTests) ... ok
test_editor (__main__.VPEUnitTests) ... ok
test_showSymbolTable (__main__.VPEUnitTests) ... ok
test_showCalendar (__main__.VPEUnitTests) ... ok
test_showASCIITable (__main__.VPEUnitTests) ... ok
test_systemShell (__main__.VPEUnitTests) ... ok
test_VGL (__main__.VPEUnitTests) ... ok
test_VEDD (__main__.VPEUnitTests) ... ok
test_routineSearch (__main__.VPEUnitTests) ... ok
test_ZP (__main__.VPEUnitTests) ... ok
test_UserList (__main__.VPEUnitTests) ... ok
test_FilemanTemplateDisplayers (__main__.VPEUnitTests) ... ok
test_FilemanHelp (__main__.VPEUnitTests) ... ok
test_KernelHelp (__main__.VPEUnitTests) ... ok
test_notes (__main__.VPEUnitTests) ... ok
test_key (__main__.VPEUnitTests) ... ok
test_param (__main__.VPEUnitTests) ... ok
test_ZD (__main__.VPEUnitTests) ... ok
test_CLH (__main__.VPEUnitTests) ... ok
test_DIC (__main__.VPEUnitTests) ... ok
test_purge (__main__.VPEUnitTests) ... ok
test_QSAVE (__main__.VPEUnitTests) ... ok
test_syntaxHighlighting (__main__.VPEUnitTests) ... ok
test_ZSAVE_ZLINK_percent (__main__.VPEUnitTests) ... ok
test_error_crash_message (__main__.VPEUnitTests) ... ok
test_RL (__main__.VPEUnitTests) ... ok
test_stopVPE (__main__.VPEUnitTests) ... ok
test_upgradeVPE (__main__.VPEUnitTests) ... ok
test_reEnterVPE (__main__.VPEUnitTests) ... ok
test_editorErrorTrap (__main__.VPEUnitTests) ... ok
test_stopVPE2 (__main__.VPEUnitTests) ... ok

----------------------------------------------------------------------
Ran 41 tests in 60.628s

OK
```

If you want to connect to a remote VistA instance, or use a username/password
with Caché, then read the code in `VistA/Python/vista/TestHelper.py`
for a hint of how to do that.

## Changes
The entire change history from version 9 to the current version can be found
[here](Changes.md).

## License
The VPE is now licensed under Apache 2.0. See [LICENSE](LICENSE) for more details.

## XINDEX
VPE passes XINDEX, with the following exceptions, from which it is exempt:

 * Fileman INIT routines don't have a correct first line (exempt under 2.2.1.2)
 * Vendor specific routine and external package calls (exempt as a Kernel Extension under 2.2.8)

## Packaging
For the maintainers, there is a set of instructions on how to make a new
release of VPE at [PACKAGING.md](PACKAGING.md).

## Future Plans
There are a ton of feature requests and bugs in the Issue Tracker. Personally
(Sam) I would wish for an integrated debugger inside of VPE.

## Ray Newman's Mumps V1 support
There is now full support as of v14.0 for MV1. However, there is a bug in MV1
where the M95 error trap behaves like the old $ZTRAP, so Error trap unwind is
handled differently for MV1.
