import unittest
import sys
import TestHelper
import cProfile, pstats
import time

TIMEOUT = .1

class VPEUnitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.vista = test_driver.connect_VistA(test_suite_details)
        cls.vista.startCoverage(test_suite_details.coverage_subset)

    @classmethod
    def tearDownClass(cls):
        cls.vista.stopCoverage(test_suite_details.result_dir + '/VPE_Coverage.cov', test_suite_details.coverage_type)
        cls.vista.write('halt')

    def test_deleteVPE(self):
        self.vista.write('D RESET^XV')
        self.vista.wait('>')

    def test_startVPE(self):
        self.vista.write('S %ut=1') # This prevents VPE from auto-resizing, which confuses pexpect
        self.vista.write('D ^XV')
        rval = self.vista.multiwait(['NAME', 'ID'])
        self.vista.write('`1')
        self.vista.wait('ID Number')
        self.vista.write('1')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('Load VPE Shell global')
        self.vista.write('Y')
        self.vista.wait('to continue..')
        self.vista.write('')
        self.assertEqual(self.vista.wait('>>'),1)

    def test_startVPE_with_v12_installed(self):
        self.vista.write('HALT')
        self.vista.wait('>')
        self.vista.write('K ^XVEMS')
        self.vista.write('D DT^DICRW')
        self.vista.write('S DIU="^XVV(19200.11,",DIU(0)="DSE" D EN^DIU2')
        self.vista.write('S DIU="^XVV(19200.111,",DIU(0)="DSE" D EN^DIU2')
        self.vista.write('S DIU="^XVV(19200.112,",DIU(0)="DSE" D EN^DIU2')
        self.vista.write('S DIU="^XVV(19200.113,",DIU(0)="DSE" D EN^DIU2')
        self.vista.write('S DIU="^XVV(19200.114,",DIU(0)="DSE" D EN^DIU2')
        self.vista.wait('>')
        self.vista.write('S %ut=1,^%ZVEMS="W BOO"') # This prevents VPE from auto-resizing, which confuses pexpect
        self.vista.wait('>')
        self.vista.write('D ^XV')
        rval = self.vista.multiwait(['NAME', 'ID'])
        self.vista.write('`1')
        self.vista.wait('ID Number')
        self.vista.write('1')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('Load VPE Shell global')
        self.vista.write('Y')
        self.vista.wait('Old VPE (v12) seems to be installed here')
        self.vista.wait('to continue..')
        self.vista.write('')
        self.assertEqual(self.vista.wait('>>'),1)
        self.vista.write('HALT')
        self.vista.wait('>')
        self.vista.write('K ^%ZVEMS')
        self.vista.wait('>')
        self.vista.write('D ^XV')
        self.vista.wait('>>')

    def test_tryStartAgainFromWithin(self):
        self.vista.write('D ^XV')
        self.assertEqual(self.vista.wait('VSHELL CURRENTLY ACTIVE'),1)
        self.assertEqual(self.vista.wait('>>'),1)

    def test_tryDUZ999999999(self):
        self.vista.write('HALT')
        self.vista.write('K  S DUZ=999999999,%ut=1 D ^XV')
        self.vista.wait('Enter ID Number: 999999999')
        self.vista.write('')
        self.assertEqual(self.vista.wait('>>'),1)
        self.vista.write('HALT')
        self.vista.write('K  S DUZ=1,%ut=1 D ^XV')
        self.assertEqual(self.vista.wait('>>'),1)

    def test_qwiks(self):
        # Test User Qwiks
        self.vista.write('.')
        self.assertTrue(self.vista.wait('No User QWIKs on record'))
        self.vista.wait('>>')

        # Test System Qwiks
        self.vista.write('..')
        boo = self.vista.wait('ZW')
        self.assertEqual(boo,1)
        self.vista.wait('>>')

        # Test ..QL1 and then Esc,H and then enter to exit and esc esc to exit
        self.vista.write('..QL1')
        self.assertEqual(self.vista.wait('U S E R   Q W I K S'),1)
        self.vista.writectrl(chr(27)) # ESC-H
        self.vista.writectrl('H')
        self.assertEqual(self.vista.wait('V P E   S C R O L L E R'),1)
        self.vista.write('')
        self.assertEqual(self.vista.wait('U S E R   Q W I K S'),1)
        self.vista.writectrl(chr(27)) # exit
        self.vista.writectrl(chr(27))
        self.vista.wait('>>')

        ## Test ..QL2 and then exit
        self.vista.write('..QL2')
        self.assertEqual(self.vista.wait('U S E R   Q W I K S'),1)
        self.vista.writectrl(chr(27)) # exit
        self.vista.writectrl(chr(27))
        self.vista.wait('>>')

        ## Test ..QL3
        self.vista.write('..QL3')
        self.assertEqual(self.vista.wait('S Y S T E M   Q W I K S'),1)
        self.assertEqual(self.vista.wait('DOS'),1)
        self.vista.writectrl(chr(27) + '[B') # Down arrow
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.vista.writectrl('F') # Find
        self.assertTrue(self.vista.wait('S C R O L L E R   F I N D   U T I L I T Y'))
        self.assertTrue(self.vista.wait('Enter CHARACTERS:'))
        self.vista.write('ZW')
        self.assertTrue(self.vista.wait('ZW'))
        self.vista.writectrl(chr(27)) # exit
        self.vista.writectrl(chr(27))
        self.vista.wait('>>')

        ## Test ..QL4
        self.vista.write('..QL4')
        self.assertEqual(self.vista.wait('S Y S T E M   Q W I K S'),1)
        self.assertEqual(self.vista.wait('DOS'),1)
        self.vista.writectrl(chr(27) + '[6~') # page down several times
        self.vista.writectrl(chr(27) + '[6~')
        self.vista.writectrl(chr(27) + '[6~')
        self.vista.writectrl(chr(27) + '[6~')
        self.assertTrue(self.vista.wait('ZW'))
        self.vista.writectrl(chr(27)) # exit
        self.vista.writectrl(chr(27))
        self.vista.wait('>>')

        ## F1-1, F1-2, F1-3, F1-4 = ..QL1,QL2,QL3,QL4
        self.vista.writectrl(chr(27) + 'OP1') # F1-1
        self.assertTrue(self.vista.wait('U S E R   Q W I K S'))
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.writectrl(chr(27) + 'OP2') # F1-2
        self.assertTrue(self.vista.wait('U S E R   Q W I K S'))
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.writectrl(chr(27) + 'OP3') # F1-3
        self.assertTrue(self.vista.wait('S Y S T E M   Q W I K S'))
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.writectrl(chr(27) + 'OP4') # F1-4
        self.assertTrue(self.vista.wait('S Y S T E M   Q W I K S'))
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        ## QWIK Boxes - I honestly didn't know about these before!
        self.vista.write('..1')
        self.vista.wait('QVL')
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.write('..2')
        self.vista.wait('VER')
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.write('..3')
        self.vista.wait('ZW')
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.write('..4')
        self.vista.wait('XQH')
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.write('..5')
        self.vista.wait('LOCKTAB')
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.write('..6')
        self.vista.wait('No System QWIKs assigned to this box.')
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        self.vista.write('.1')
        self.vista.wait('No User QWIKs assigned to this box.')
        self.vista.writectrl(chr(27) + chr(27))
        self.vista.wait('>>')

        ## QWIK Autocomplete
        self.vista.write('..FM')
        self.vista.wait('Fileman Sort Template')
        self.vista.write('')
        self.vista.wait('>>')


    def test_command_line_shortcuts(self):
        # Left Arrow - Load command line history
        self.vista.writectrl(chr(27) + '[D')
        self.assertTrue(self.vista.wait('7) ..QL4')) # 6th command is QL4
        self.assertTrue(self.vista.wait('Select:'))
        self.vista.write('7')
        self.vista.write('')
        self.assertEqual(self.vista.wait('S Y S T E M   Q W I K S'),1)
        self.vista.writectrl(chr(27)) # exit
        self.vista.writectrl(chr(27))
        self.vista.wait('>>')

        # Up Arrow - Recall last command
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.assertTrue(self.vista.wait('..QL4'))
        self.vista.write('')
        self.assertEqual(self.vista.wait('S Y S T E M   Q W I K S'),1)
        self.vista.writectrl(chr(27)) # exit
        self.vista.writectrl(chr(27))
        self.vista.wait('>>')

        # Down Arrow - Recall first command
        self.vista.writectrl(chr(27) + '[B') # Down arrow
        self.assertTrue(self.vista.wait('D ^XV'))
        self.vista.writectrl(chr(27) + '[A') # Up arrow to cancel
        self.assertTrue(self.vista.wait('>>'))

    def test_command_line_error_trap(self):
        self.vista.write('W 1/0')
        self.assertTrue(self.vista.wait('ERROR LINE/CODE: '))
        self.vista.wait('>>')

    def test_command_line_global_warn(self):
        self.vista.write('K ^SAMSAMSAM')
        self.assertTrue(self.vista.wait('Should I execute your code: NO//'))
        self.vista.write('Y')
        self.vista.wait('>>')
        self.vista.write('K ^SAMSAMSAM')
        self.assertTrue(self.vista.wait('Should I execute your code: NO//'))
        self.vista.write('N')
        self.assertTrue(self.vista.wait('Code not executed...'))
        self.vista.wait('>>')

    def test_main_help(self):
        self.vista.writectrl(chr(27) + 'H') # ESC-H
        self.assertTrue(self.vista.wait('V S H E L L   H E L P   M E N U'))
        self.assertTrue(self.vista.wait('SELECT:'))
        self.vista.writectrl(chr(27) + '[B') # Down arrow - select Protection
        self.vista.write('') # enter
        self.assertTrue(self.vista.wait('P R O T E C T I O N'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('V S H E L L   H E L P   M E N U'))
        self.assertTrue(self.vista.wait('SELECT:'))

        self.vista.write('Misc') # Look for new help text (v15.0)
        self.vista.wait('M I S C E L L A N E O U S') 
        self.vista.writectrl(chr(27) + '[6~')
        self.vista.wait('')
        self.vista.writectrl(chr(27) + '[6~')
        self.vista.wait('Highlight Syntax') 
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.write('Quit')
        self.assertTrue(self.vista.wait('>>'))

    def test_delete_routine(self):
        self.vista.write('..ZR KBANTEST KBANFOO')
        boo = self.vista.wait('OK TO DELETE?')
        self.assertEqual(boo,1)
        self.vista.write('Y')
        boo = self.vista.wait('Removed')
        self.assertEqual(boo,1)
        self.vista.wait('>>')

    def test_editor(self):
        # Create new routine KBANTEST
        self.vista.write('..E')
        self.vista.wait('ROUTINE')
        self.vista.write('KBANTEST')
        self.vista.wait('^KBANTEST]')
        self.vista.write('')
        self.vista.write('KBANTEST' + chr(9) + '; TEST ROUTINE')
        self.vista.write(chr(9) + 'D USEZERO^XVEMSU')
        self.vista.write(' W "HELLO VPE",!')
        self.vista.write(' QUIT')
        self.vista.write('TAG1' + chr(9) + '; TEST TAG')
        self.vista.write(chr(9) + 'N Z')
        self.vista.wait('Z')
        for x in range(0,81):
            self.vista.write(' S Z=1')
            self.vista.wait('=============')
        self.vista.write(' D USEZERO^XVEMSU')
        self.vista.write(' W "BYE VPE",!')
        self.vista.write(' QUIT')
        self.vista.wait('T')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel line
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.write('')
        self.vista.wait('saved to disk')
        self.vista.wait('>>')
        self.vista.write('D ^KBANTEST')
        self.vista.wait('HELLO VPE')
        self.vista.wait('>>')

        # View routine using ..VRR
        self.vista.write('..VRR KBANTEST')
        self.vista.wait('^KBANTEST]')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('>>')

        # View routine using ..VRR two arguments to jump to tag & Keyboard Help
        self.vista.write('..VRR KBANTEST TAG1')
        self.vista.wait('TAG1')
        self.vista.writectrl(chr(27) + 'K') # Keyboard help
        self.vista.wait('Cursor up 1 line')
        self.vista.writectrl(chr(27) + chr(27)) # Exit Help
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('>>')
        
        # Test keyboard shortcuts
        self.vista.write('..E KBANTEST')
        self.vista.wait('^KBANTEST]')
        self.vista.writectrl(chr(27) + 'OS' + chr(27) + '[D') # F4 Left Arrow - Go to first line
        self.vista.writectrl(chr(27) + '[B') # Down arrow once
        self.vista.writectrl(chr(27) + 'OR') # F3 - Turn on highlighting
        for x in range (0,3): # Down arrow three times
            self.vista.writectrl(chr(27) + '[B')
        self.vista.writectrl(chr(27) + 'C') # Esc-C copy to clipboard
        self.vista.writectrl(chr(27) + 'V') # Esc-V paste
        for x in range (0,3): # Down arrow three times
            self.vista.writectrl(chr(27) + '[B')
        self.vista.writectrl(chr(27) + 'D') # Esc-D delete line
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.vista.write('')
        self.vista.write(' W ^VA(200,0)')
        self.vista.wait('^')
        self.vista.writectrl(chr(27) + chr(27)) # Exit

        # ESC-G tests: New and improved in V15.0
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + '[D') # F1 + Left arrow : Now on W
        self.vista.writectrl(chr(27) + '[C') # Right arrow twice                : Now on space
        self.vista.writectrl(chr(27) + '[C') # Right arrow twice                : Now on ^
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait('NEW PERSON')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('^KBANTEST]')
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on V
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on A
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on (
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait('DUPLICATE RECORD')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('^KBANTEST]')
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on 2
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on 0
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on 0
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on ,
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait('NEW PERSON')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('^KBANTEST]')
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on 0
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on )
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait('NEW PERSON')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('^KBANTEST]')
        self.vista.writectrl(chr(27) + '[D') # Left arrow                      : Now on 0
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait(chr(7))

        # Test long parsing globals on long lines that cross 80 margin boundary
        # This stanza is for parsing backwards
        self.vista.write('')
        self.vista.write(' K ^UTILITY("DIQ1",$J) S DA=$P($$SITE^VASITE(),"^") I $G(DA) S DIC=4,DIQ(0)="I",DR="99" D EN^DIQ1 S PSOINST=$G(^UTILITY("DIQ1",$J,4,DA,99,"I")) K ^UTILITY("DIQ1",$J),DA,DR,DIC')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel next line
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + 'OP') # F1 + F1 : Now on beginning of 3rd line of full code line on I of ^UTILITY("DIQ1"...)
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on "
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on )
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait('^UTILITY("DIQ1",$J,4,:,99,"I"') # Should say that this global has no data
        self.vista.write('')                             # Exit press return to continue
        self.vista.wait('^KBANTEST]')

        # This stanza is for parsing forwards
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.vista.writectrl(chr(27) + 'OQ' + chr(27) + 'OQ') # F2 F2 to go to end of line
        self.vista.writectrl(chr(27) + 'OQ' + chr(27) + '[D') # F2 + Left Arrow once (short jump)
        self.vista.writectrl(chr(27) + 'OQ' + chr(27) + '[D') # F2 + Left Arrow twice (short jump) on G of $G now
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on (
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on ^
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait('^UTILITY("DIQ1",$J,4,:,99,"I"') # Should say that this global has no data
        self.vista.write('')                             # Exit press return to continue
        self.vista.wait('^KBANTEST]')

        # This stanza is for parsing backwards to global and forward to get the rest of the reference
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on U
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on T
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on I
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on L
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on I
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on T
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on Y
        self.vista.writectrl(chr(27) + '[C') # Right arrow                      : Now on (
        self.vista.writectrl(chr(27) + 'G')  # Get global
        self.vista.wait('Session 1 ^UTILITY')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('^KBANTEST]')


        # Test parsing dollar functions + parens
        self.vista.write('')
        self.vista.write(' I $P($G(RXFL(RX)),"^"),$D(^PSRX(RX,1,$P($G(RXFL(RX)),"^"),0)) K RXY,RXP,REPRINT Q')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel next line
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + '[D') # F1 Left Arrow - Go to beginning of line
        self.vista.writectrl(chr(27) + 'OQ' + chr(27) + '[C') # F2 + Right Arrow once (short jump)
        self.vista.writectrl(chr(27) + 'OQ' + chr(27) + '[C') # F2 + Right Arrow twice (short jump) on X of ^PSRX
        self.vista.writectrl(chr(27) + '[D') # Left arrow                      : Now on R
        self.vista.writectrl(chr(27) + '[D') # Left arrow                      : Now on S
        self.vista.writectrl(chr(27) + '[D') # Left arrow                      : Now on P
        self.vista.writectrl(chr(27) + '[D') # Left arrow                      : Now on ^
        self.vista.writectrl(chr(27) + 'G')  # Get Global
        self.vista.wait('^PSRX(:,1,:')
        try:
          self.vista.wait('<> <> <>', TIMEOUT)
          self.vista.writectrl(chr(27) + chr(27)) # There is data, exit
        except:
          self.vista.write('')                    # Exit press return to continue
        self.vista.wait('^KBANTEST]')

        # ESC-R Tests
        # Test 1: Regular ESC-R on the level line (not continuation) to another routine
        # Move 3 up
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.vista.writectrl(chr(27) + '[A') # Up arrow  - Now on = in S DA=$P($$SITE^VASITE() of above line
        self.vista.writectrl(chr(27) + 'OQ' + chr(27) + '[C') # F2 + Right Arrow once (short jump) # Now on T of SITE
        for x in range (0,5): self.vista.writectrl(chr(27) + '[D') # Left Arrow 5 times. Now on ^.
        self.vista.writectrl(chr(27) + 'R') # ESC-R
        self.vista.wait('VASITE]')          # New Routine
        self.vista.writectrl(chr(27) + chr(27))  # ESC-ESC
        self.vista.wait('KBANTEST]')
        
        # Test 2: Regular ESC-R on a continuation line
        self.vista.write('')
        self.vista.write(' .I DIV]"",^DD(DIH,DIG,"AUDIT")\'="e"!(DIU]"") S X=DIV,DIIX=3_U_DIG,DP=DIH D AUDIT^DIET ;Don\'t audit NEW if there\'s no OLD and mode is EDIT ONLY')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel next line
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + '[D') # F1 Left Arrow - Go to beginning of line
        self.vista.writectrl(chr(27) + '[B') # Down arrow # Now on DIH
        for x in range (0,11): self.vista.writectrl(chr(27) + '[C') # Right Arrow 11 times. Now on ^.
        self.vista.writectrl(chr(27) + 'R') # ESC-R
        self.vista.wait('DIET]')
        self.vista.writectrl(chr(27) + chr(27))  # ESC-ESC
        self.vista.wait('KBANTEST]')

        # Test 3: ESC-R on a Tag across line boundary going forward
        self.vista.write('')
        self.vista.write(' I DIV]"" F DIW=0:0 S DIW=$O(^DD(DIH,DIG,1,DIW)),X=DIV Q:\'DIW  I $P(^(DIW,0),U,3)=""!\'$D(DB(0,DIH,DIG,DIW,1)) S DB(0,DIH,DIG,DIW,1)=1 D TAG1 X ^(1) D TAG1')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel next line
        # Looks like this now:
        # 23       I DIU]"" F DIW=0:0 S DIW=$O(^DD(DIH,DIG,1,DIW)),X=DIU Q:'DIW  I $P(^(
        #          DIW,0),U,3)=""!'$D(DB(0,DIH,DIG,DIW,2)) S DB(0,DIH,DIG,DIW,2)=1 D TAG
        #          1 X ^(2) D TAG1
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.vista.writectrl(chr(27) + 'OQ' + chr(27) + 'OQ') # F2 F2 to go to end of line just beyond TAG
        self.vista.writectrl(chr(27) + '[D') # Left arrow                      : Now on G of TAG
        self.vista.writectrl(chr(27) + 'R') # ESC-R
        self.vista.wait('TAG1')
        self.vista.writectrl(chr(27) + chr(27)) # Go back to original level
        self.vista.wait('KBANTEST]')

        # Test 4: ESC-R on a Tag across line boundary going backwards
        # Start on G of TAG on line 2
        self.vista.writectrl(chr(27) + '[B') # Down arrow
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + 'OP') # F1-F1 to beginning of line. Now on 1 of the 3rd line
        self.vista.writectrl(chr(27) + 'R') # ESC-R
        self.vista.wait('TAG1')
        self.vista.writectrl(chr(27) + chr(27)) # Go back to original level
        self.vista.wait('KBANTEST]')

        # Test 5: ESC-R on a Routine Tag going backwards
        # NB: Can't get it to work. Not sure why, but not spending more time.
        # 11       I DIV]"" F DIW=0:0 S DIW=$O(^DD(DIH,DIG,1,DIW)),X=DIV Q:'DIW  I $P(^(
        #          DIW,0),U,3)=""!'$D(DB(0,DIH,DIG,DIW,1)) S DB(0,DIH,DIG,DIW,1)=11 D PI
        #          D^VADPT
        #self.vista.write('')
        #self.vista.write(' I DIV]"" F DIW=0:0 S DIW=$O(^DD(DIH,DIG,1,DIW)),X=DIV Q:\'DIW  I $P(^(DIW,0),U,3)=""!\'$D(DB(0,DIH,DIG,DIW,1)) S DB(0,DIH,DIG,DIW,1)=11 D PID^VADPT')
        #self.vista.wait('T')
        #self.vista.writectrl(chr(27) + chr(27)) # Cancel next line
        #self.vista.writectrl(chr(27) + 'OP' + chr(27) + 'OP') # F1-F1 to beginning of line. Now on D of D^VADPT.
        #self.vista.writectrl(chr(27) + '[C') # Right arrow. Now on ^.
        #self.vista.writectrl(chr(27) + 'R') # ESC-R
        #self.vista.wait('[PID^VADPT]')
        #self.vista.writectrl(chr(27) + chr(27)) # Go back to original level
        #self.vista.wait('KBANTEST]')

        # Home and End
        self.vista.write(chr(27) + '[H') # Home
        self.vista.write(chr(27) + '[F') # End
        self.vista.wait('QUIT')

        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.writectrl(chr(27) + '[C') # Right arrow to get to SAVE_AS
        self.vista.write('')
        self.vista.wait('Save as routine')
        self.vista.write('KBANFOO')
        self.vista.wait('KBANFOO saved to disk.')
        self.vista.wait('>>')

        # Test tab commands. This goes on for a while!!!!
        self.vista.write('..E KBANTEST')
        self.vista.wait('^KBANTEST]')

        ## F - Find
        self.vista.write(chr(9) + 'F') # Find
        self.vista.wait('TAG1')
        self.vista.write('1')

        ## R - Branch to Routine
        self.vista.write(chr(9) + 'R') # Branch to Routine
        self.vista.wait('BRANCH TO A ROUTINE')
        self.vista.write('XV')
        self.vista.wait('^XV]')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.wait('^KBANTEST]')

        # L - Locate String + ESC-N to find next instance
        self.vista.writectrl(chr(27) + 'OS' + chr(27) + '[C') # F4 Right Arrow - Go to end
        self.vista.wait('<> <> <>')
        self.vista.writectrl(chr(27) + 'OS' + chr(27) + '[D') # F4 Left Arrow - Go to home
        self.vista.wait('TEST ROUTINE')
        self.vista.write(chr(9) + 'L') # Locate string
        self.vista.wait('STRING:')
        self.vista.write('XVEMSU')      # Find first instance
        self.vista.write(chr(27) + 'N') # Find next instance
        self.vista.wait('USEZERO')
        self.vista.writectrl(chr(27) + chr(27)) # Don't know why that's needed?! Am I not finding the next thing?

        # Goto line
        self.vista.write(chr(9) + 'G') # Goto
        self.vista.wait('LINE')
        self.vista.write('20') # Goto
        self.vista.wait('30') # 30 should be visible

        # Help
        self.vista.write(chr(9) + '?') # Help
        self.vista.wait('N O T E S')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.wait('^KBANTEST]')


        self.vista.writectrl(chr(27) + 'OS' + chr(27) + '[C') # F4 Right Arrow - Go to end
        self.vista.wait('<> <> <>')
        self.vista.write(chr(9) + 'CALL') # Goto
        self.vista.wait('**INSERT PROGRAMMER CALL***')
        self.vista.write('DBS DIC $$FIND')
        self.vista.wait('Delete previous values?')
        self.vista.write('')
        self.vista.wait('CONSTRUCT & INSERT PROGRAMMER CALL')
        self.vista.writectrl('1' + chr(9))
        self.vista.wait('H=Help')
        self.vista.write('')
        self.vista.writectrl('1,' + chr(9))
        self.vista.wait('H=Help')
        self.vista.write('')
        self.vista.writectrl('PX')
        self.vista.writectrl(chr(27) + 'OPE') # F1-E to save and exit
        self.vista.wait('Insert this Call into your routine?')
        self.vista.write('')
        self.vista.wait('<> <> <>')

        self.vista.write(chr(9) + 'I') # Run XINDEX
        self.vista.wait('C R O S S  R E F E R E N C E R')
        self.vista.write('')
        self.vista.wait('Compiled list of Errors and Warnings')
        self.vista.write('')
        self.vista.wait('<> <> <>')

        self.vista.write(chr(9) + 'S') # Get Routine Size
        self.vista.wait('Routine size =')
        self.vista.write('')

        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')

        self.vista.writectrl(chr(27) + chr(27)) # v15.0 <- This should have no effect - We disabled ESC-ESC from routines
        self.vista.wait('SAVE_AS')
        self.vista.writectrl(chr(27) + chr(27)) # v15.0 <- This should have no effect - We disabled ESC-ESC from routines
        self.vista.wait('SAVE_AS')
        self.vista.writectrl(chr(27) + chr(27)) # v15.0 <- This should have no effect - We disabled ESC-ESC from routines
        self.vista.wait('SAVE_AS')

        finished = 0
        while not finished:
            try:
                self.vista.wait('saved', TIMEOUT)
            except:
                finished = 1
        self.assertTrue(finished)
        self.vista.write('Q')
        self.vista.wait('>>')

    def test_showSymbolTable(self):
        self.vista.write('..ZW')
        self.assertTrue(self.vista.wait('%ut')) # We put this guy in at the very beginning
        self.vista.writectrl(chr(27) + chr(27)) # exit
        self.vista.wait('>>')
        self.vista.write('..ZW X') # Start symbol table at a specific variable
        self.assertTrue(self.vista.wait('X')) # We put this guy in at the very beginning
        self.vista.writectrl(chr(27) + chr(27)) # exit
        self.vista.wait('>>')

    def test_showCalendar(self):
        self.vista.write('..CAL')
        self.assertTrue(self.vista.wait('S I X   M O N T H   P L A N N E R'))
        self.vista.wait('>>')

    def test_showASCIITable(self):
        self.vista.write('..ASCII')
        self.assertTrue(self.vista.wait('A S C I I   C H A R A C T E R   S E T'))
        self.vista.wait('>>')

    def test_systemShell(self):
        self.vista.write('..DOS')
        rval = self.vista.multiwait(['@', 'Not available for this M Vendor.'])
        if (rval == 0): self.vista.write('exit')
        self.assertTrue(self.vista.wait('>>'))

    def test_VGL(self):
        # Direct routine call and exit
        self.vista.write('D ^XVEMG')
        self.vista.wait('Global')
        self.vista.write('')
        self.assertTrue(self.vista.wait('>>'))

        # Regular ..VGL on File 200
        self.vista.write('..VGL')
        self.vista.wait('Global')
        self.vista.write('VA(200,')
        self.vista.wait('^VA(200,.5,0)')

        # Test tab key
        self.vista.writectrl(chr(9))
        self.vista.wait('INTERNAL VALUE')
        self.vista.writectrl(chr(27) + chr(27)) # Go back

        # Test show file header
        self.vista.write('1')
        self.assertTrue(self.vista.wait('Global Pieces(INT VALUE)'))
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.wait('^VA(200,.5,0)')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.wait('Global')

        # Up arrow to recall last global, then zero nodes
        self.vista.writectrl(chr(27) + '[A') # Up arrow
        self.vista.wait('^VA')
        self.vista.write(',:,0)') # Just get the zero nodes
        self.vista.wait('^VA(200,1,0)')
        self.vista.write('10') # regular node select
        self.vista.wait('TITLE')
        self.vista.write('9') # Title DD
        self.vista.wait('^DIC(3.1,')
        self.assertTrue(self.vista.wait('CONTINUE'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('CONTINUE'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.write('') # Now out of the title DD

        self.vista.write('X') # External Values
        self.assertTrue(self.vista.wait('EXTERNAL VALUE'))
        self.vista.write('I') # Internal Values
        self.assertTrue(self.vista.wait('INTERNAL VALUE'))
        self.vista.write('?') # Help
        self.assertTrue(self.vista.wait('Enter number from center column'))
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.write('') # End of Help
        self.vista.writectrl(chr(27) + 'H') # Scroll Help
        self.assertTrue(self.vista.wait('<ARROW DOWN>'))
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.write('') # Now out of Scroll Help
        self.assertTrue(self.vista.wait('Termination Reason'))
        
        self.vista.writectrl(chr(27) + chr(27)) # Go back to global lister
        self.vista.wait('^VA(200,.5,0)')

        # Alternate Session - Select by file
        self.vista.write('A')
        self.vista.wait('Session 2')
        self.vista.write(' ')
        self.vista.wait('Select FILE:')
        self.vista.write('PARAMETER DEF')
        self.vista.wait('^XTV(8989.51,')
        self.vista.write('')
        self.vista.wait('^XTV(8989.51,1,0)')
        # Page Down twice
        self.vista.writectrl(chr(27) + '[6~')
        self.vista.wait('')
        self.vista.writectrl(chr(27) + '[6~')
        self.vista.wait('')
        # Page up twice
        self.vista.writectrl(chr(27) + '[5~')
        self.vista.wait('')
        self.vista.writectrl(chr(27) + '[5~')
        self.vista.wait('')
        # Goto node 30
        self.vista.write('G')
        self.vista.wait('REF NUMBER')
        self.vista.write('30')
        self.vista.multiwait(['8989.51,3','8989.51,4'])

        # Exit Session 2
        self.vista.writectrl(chr(27) + chr(27)) # back to Session 2 prompt
        self.vista.wait('Session 2')
        self.vista.writectrl(chr(27) + chr(27)) # back to Session 1
        self.vista.wait('^VA(200,.5,0)')

        # Exit Session 1
        self.vista.writectrl(chr(27) + chr(27)) # Exit session 1
        self.vista.wait('Global')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))

        # Reverse Video subscripts entry point
        self.vista.write('S DUZ(0)="#"')
        self.vista.write('D R^XVEMG')
        self.vista.wait('Global')
        self.vista.write('VA(200,')
        self.vista.wait('^VA(200,' + chr(27) + '[7m ' + '.5 ' + chr(27))
        finished = 0
        while not finished:
            try:
                self.vista.wait('^VA(200,' + chr(27) + '[7m ' + '1 ' + chr(27), TIMEOUT)
                finished = 1
            except:
                self.vista.write('S2') # Skip down until the second sub changes

        self.vista.write('C') # Command search will fail
        self.vista.wait('You don\'t have access.')
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.write('')

        self.vista.write('?') # Help
        self.vista.wait('left hand column')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.wait('^VA(200,' + chr(27) + '[7m ' + '1 ' + chr(27))

        self.vista.write('M') # More...
        self.vista.wait('Call VGL at R^XVEMG to display subscript')
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.write('')
        self.vista.wait('^VA(200,' + chr(27) + '[7m ' + '1 ' + chr(27))
        

        # Exit Session 1
        self.vista.writectrl(chr(27) + chr(27)) # Exit session 1
        self.vista.wait('Global')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))

        # Go back in, with parameters this time, but set DUZ(0)="@" first.
        # Then run C for command search
        self.vista.write('S DUZ(0)="@"')
        self.vista.wait('>>')
        self.vista.write('..VGL ^VA(200,')
        self.vista.wait('^VA(200,.5,0)')
        self.vista.write('C')
        self.vista.wait('Enter Mumps Code')
        self.vista.write('I $P(GLSUB,')
        self.vista.wait('There is an error in your code.')
        self.vista.write('I $P(GLSUB,",",3)=.1') # This grabs all users with verify codes
        self.vista.wait('CODE SEARCH IN PROGRESS..')
        self.vista.wait('^VA(200,1,.1)')
        self.vista.writectrl(chr(32)) # this just stops the search
        finished = 0
        while not finished:
            try:
                self.vista.wait('>>', TIMEOUT)
                finished = 1
            except:
                self.vista.writectrl(chr(27) + chr(27)) # Go to command line

        # Test * syntax
        self.vista.write('..VGL ^VA*')
        self.assertTrue(self.vista.wait('STATION NUMBER (TIME SENSITIVE)'))
        self.assertTrue(self.vista.wait('Enter NODE Number'))
        self.vista.write('7')
        self.assertTrue(self.vista.wait('APPLICATION PROXY'))
        self.vista.writectrl(chr(27) + chr(27)) # Go to command line
        self.vista.wait('>>')

        # Edit Range (ER) -- Use ^TMP($J)
        # Change LINE into WINE
        self.vista.write('K ^TMP($J)')
        self.vista.wait('Should I execute your code:')
        self.vista.write('Y')
        self.vista.wait('>>')
        self.vista.write('S ^TMP($J,1)="LINE 1"')
        self.vista.wait('>>')
        self.vista.write('S ^TMP($J,2)="LINE 2"')
        self.vista.wait('>>')
        self.vista.write('S ^TMP($J,3)="LINE 3"')
        self.vista.wait('>>')
        self.vista.write('..VGL ^TMP($J')
        self.vista.wait('LINE 3')
        self.vista.write('ER')
        self.vista.wait('REF NUMBER')
        self.vista.write('1-3')
        self.vista.wait('Replace')
        self.vista.write('LINE')
        self.vista.wait('With')
        self.vista.write('WINE')
        self.vista.wait('Select')
        self.vista.writectrl(chr(27) + chr(27)) # Go to command line
        self.vista.wait('>>')
        self.vista.write('..VGL ^TMP($J')
        self.vista.wait('WINE 3')
        self.vista.writectrl(chr(27) + chr(27)) # Go to command line
        self.vista.wait('>>')

        # Edit Subscript. Second Line change 2 to "BOO"
        self.vista.write('..VGL ^TMP($J')
        self.vista.wait('WINE 3')
        self.vista.write('ES')
        self.vista.wait('REF NUMBER')
        self.vista.write('2')
        self.vista.writectrl(chr(8)) # backspace
        self.vista.write('"')
        self.vista.wait('Invalid subscript.')
        self.vista.write('')
        self.vista.wait('WINE 3')
        self.vista.write('ES')
        self.vista.wait('REF NUMBER')
        self.vista.write('2')
        self.vista.writectrl(chr(8)) # backspace
        self.vista.write('"BOO"')
        self.vista.wait(',"BOO")')
        self.vista.writectrl(chr(27) + chr(27)) # Go to command line
        self.vista.wait('>>')

        # Edit Subscript. Second Line (now 3) change 3 to "BOO". Should block us.
        self.vista.write('..VGL ^TMP($J')
        self.vista.wait('WINE 3')
        self.vista.write('ES')
        self.vista.wait('REF NUMBER')
        self.vista.write('2')
        self.vista.writectrl(chr(8)) # backspace
        self.vista.write('"BOO"')
        self.vista.wait('This node already exists.')
        self.vista.write('')
        self.vista.writectrl(chr(27) + chr(27)) # Go to command line
        self.vista.wait('>>')

        # Edit Value. Third line change from WINE 2 to FINE 5
        self.vista.write('..VGL ^TMP($J')
        self.vista.wait('WINE 3')
        self.vista.write('EV')
        self.vista.wait('REF NUMBER')
        self.vista.write('2')
        for i in range(0,6):
            self.vista.writectrl(chr(8)) # backspace over WINE 2
        self.vista.write('FINE 5')
        self.vista.wait('FINE 5')
        self.vista.writectrl(chr(27) + chr(27)) # Go to command line
        self.vista.wait('>>')

        # Run Global Parser M-Unit Tests
        self.vista.write('DO TEST^XVEMREP')
        self.vista.wait('Checked 4 tests, with 0 failures and encountered 0 errors.')
        self.vista.wait('>>')


    def test_VEDD(self):
        # Set DUZ(0) to contain # for VGL
        self.vista.write('S DUZ(0)="#"')
        self.vista.wait('>>')
        # Test entry and exit from VEDD
        self.vista.write('..VEDD')
        self.assertTrue(self.vista.wait('FILE:'))
        self.vista.write('52')
        self.assertTrue(self.vista.wait('PRESCRIPTION'))
        self.assertTrue(self.vista.wait('Select OPTION:'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('Select FILE:'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))
        
        # Go back in
        self.vista.write('..VEDD 52')
        self.assertTrue(self.vista.wait('PRESCRIPTION'))
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Test listing indexes (X)
        self.vista.write('X')
        self.assertTrue(self.vista.wait('ACRO')) # name of first index on my screen
        finished = 0
        while not finished:  # *I think there is a race condition here between the try and the except*
            # What I have here *shouldn't* work except if the 'except' takes place more often than the try
            try:
                self.vista.wait('MAIN_MENU',TIMEOUT)
                finished = 1
            except:
                self.vista.write('')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Test listing Pointers In (PI)
        self.vista.write('PI')
        self.assertTrue(self.vista.wait('DUE ANSWER SHEET')) # name of pointer file
        finished = 0
        while not finished:
            try:
                self.vista.wait('MAIN_MENU',TIMEOUT)
                finished = 1
            except:
                self.vista.write('')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Test listing Points Out (PO)
        self.vista.write('PO')
        self.assertTrue(self.vista.wait('NEW PERSON')) # name of pointer file
        finished = 0
        while not finished:
            try:
                self.vista.wait('MAIN_MENU',TIMEOUT)
                finished = 1
            except:
                self.vista.write('')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Test listing of Groups
        self.vista.write('GR')
        self.assertTrue(self.vista.wait('IHS')) # name of a group
        finished = 0
        while not finished:
            try:
                self.vista.wait('MAIN_MENU',TIMEOUT)
                finished = 1
            except:
                self.vista.write('')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Test Tracing of Field
        self.vista.write('TR')
        self.assertTrue(self.vista.wait('Enter Field Name'))
        self.vista.write('DRUG')
        self.assertTrue(self.vista.wait('DRUG  (6)'))
        self.vista.write('1')
        self.vista.wait('MAIN_MENU')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Test individual field DD
        self.vista.write('I')
        self.assertTrue(self.vista.wait('Select FIELD:'))
        self.vista.write('6')
        self.assertTrue(self.vista.wait('FIELD NAME:       DRUG'))
        finished = 0
        while not finished:
            try:
                self.vista.wait('Select FIELD:',TIMEOUT)
                finished = 1
            except:
                self.vista.write('')
        self.vista.write('')
        self.vista.write('I')
        self.assertTrue(self.vista.wait('Select FIELD:'))
        self.vista.write('SIG')
        self.assertTrue(self.vista.wait('SIG1'))
        self.vista.write('2')
        self.assertTrue(self.vista.wait('Select SUBFIELD:'))
        self.vista.write('?')
        self.assertTrue(self.vista.wait('Select SUBFIELD:'))
        self.vista.write('1')
        self.assertTrue(self.vista.wait('Select SUBFIELD:'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select FIELD:'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Test Fld Global Location (big!)
        self.vista.write('G')
        self.assertTrue(self.vista.wait('ALL_FIELDS'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('N=Node'))

        ## Test Obtaining a single node
        self.vista.write('8') # Trade Name
        self.assertTrue(self.vista.wait('TRADE NAME'))
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('N=Node'))

        ## Test ?
        self.vista.write('?') # Help
        self.assertTrue(self.vista.wait('Exit VEDD completely'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('N=Node'))
        
        ## Test Goto. Need to load all the file first using Page down
        ## Page down to the bottom
        for x in range(0, 20):
            self.vista.writectrl(chr(27) + '[6~')
        self.assertTrue(self.vista.wait('<> <> <>'))
        ## Page up to the top
        for x in range(0, 20):
            self.vista.writectrl(chr(27) + '[5~')
        self.assertTrue(self.vista.wait('RX #'))
        ## Goto node 100
        self.vista.write('G') # Goto
        self.assertTrue(self.vista.wait('REF NUMBER:'))
        self.vista.write('100')
        self.assertTrue(self.vista.wait('105'))

        ## Test Node
        self.vista.write('N') # Node
        self.assertTrue(self.vista.wait('NODE:'))
        self.vista.write('?') # help me
        self.assertTrue(self.vista.wait(' P '))
        self.vista.write('P') # P node
        self.assertTrue(self.vista.wait('SUBNODE'))
        self.vista.write('?') # help me
        self.assertTrue(self.vista.wait('0  1'))
        self.vista.write('1') # 1 node
        self.assertTrue(self.vista.wait('BINGO WAIT TIME'))
        self.vista.write('9') # 9 field
        self.assertTrue(self.vista.wait('<RETURN>'))
        self.vista.write('') # exit
        self.vista.multiwait(['FIELD','SUB-FIELD'])
        self.vista.write('') # exit
        self.assertTrue(self.vista.wait('SUBNODE'))
        self.vista.write('') # exit
        self.assertTrue(self.vista.wait('N=Node'))

        ## Test Pointer
        self.vista.write('P')
        self.assertTrue(self.vista.wait('REF NUMBER:'))
        self.vista.write('3') # help me
        self.assertTrue(self.vista.wait('DATE OF BIRTH'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        ## Page up to the top
        for x in range(0, 7):
            self.vista.writectrl(chr(27) + '[5~')
        self.assertTrue(self.vista.wait('RX #'))

        # Exit G
        self.vista.writectrl(chr(27) + chr(27)) # Go back

        # Templates - T
        self.vista.write('T')
        self.assertTrue(self.vista.wait('PRINT TEMPLATES')) # name of a group
        rval = 0
        while rval == 0:
            rval = self.vista.multiwait(['CONTINUE','MAIN_MENU'])
            if rval == 0: self.vista.write('')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # File Description
        self.vista.write('D')
        self.assertTrue(self.vista.wait('File description for PRESCRIPTION file.'))
        self.vista.wait('MAIN_MENU')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # File Characteristics
        self.vista.write('C')
        self.assertTrue(self.vista.wait('IDENTIFIERS:'))
        finished = 0
        while not finished:
            try:
                self.vista.wait('MAIN_MENU',TIMEOUT)
                finished = 1
            except:
                self.vista.write('')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Required Fields
        self.vista.write('R')
        self.assertTrue(self.vista.wait('RX #'))
        finished = 0
        while not finished:
            try:
                self.vista.wait('MAIN_MENU',TIMEOUT)
                finished = 1
            except:
                self.vista.write('')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # VGL - Don't run though. We will test later
        self.vista.write('VGL')
        self.assertTrue(self.vista.wait('...Global ^'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # H - Help
        self.vista.write('H')
        self.assertTrue(self.vista.wait('Bypasses opening screen.'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # PR - Turn printing mode on and try these options
        for option in [ 'X', 'PI', 'PO', 'GR' , 'T', 'C', 'R']:
            self.vista.write('PR')
            self.assertTrue(self.vista.wait('DEVICE'))
            self.vista.write('NULL')
            self.assertTrue(self.vista.wait('Select OPTION:'))
            self.vista.write(option)
            self.assertTrue(self.vista.wait('Select OPTION:'))

        # PR - Turn printing mode on and use 'I' which requires some user interaction
        self.vista.write('PR')
        self.assertTrue(self.vista.wait('DEVICE'))
        self.vista.write('NULL')
        self.assertTrue(self.vista.wait('Select OPTION:'))
        self.vista.write('I')
        self.assertTrue(self.vista.wait('Select FIELD:'))
        self.vista.write('.01')
        self.vista.write('1')
        self.vista.write('2')
        self.vista.write('3')
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # PR - Turn printing mode on and use 'G' which requires some user interaction
        self.vista.write('PR')
        self.assertTrue(self.vista.wait('DEVICE'))
        self.vista.write('NULL')
        self.assertTrue(self.vista.wait('Select OPTION:'))
        self.vista.write('G')
        self.vista.write('')
        try:
            self.vista.wait('MAIN_MENU',TIMEOUT)
            self.vista.write('') # Cache only
        except:
            pass
        
        self.vista.write('')
        self.assertTrue(self.vista.wait('Select OPTION:'))

        # Exit VEDD
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))

        # Enter VEDD via published entry point and display the data in File 60
        self.vista.write(' D ^XVEMD')
        self.assertTrue(self.vista.wait('VElectronic Data Dictionary'))
        self.assertTrue(self.vista.wait('Select FILE:'))
        self.vista.write('60')
        self.assertTrue(self.vista.wait('Select OPTION:'))
        self.vista.write('G')
        self.vista.write('')
        self.assertTrue(self.vista.wait('N=Node'))
        self.vista.write('DA')
        self.assertTrue(self.vista.wait('REF NUMBERS(S):'))
        self.vista.write('1')
        self.assertTrue(self.vista.wait('DISPLAY TYPE'))
        self.vista.write('?')
        self.assertTrue(self.vista.wait('DISPLAY TYPE'))
        self.vista.write('')
        self.assertTrue(self.vista.wait('LABORATORY TEST NAME'))
        self.vista.write('`1')
        self.assertTrue(self.vista.wait('D A T A   D I S P L A Y'))
        self.assertTrue(self.vista.wait('File: LABORATORY TEST'))
        self.assertTrue(self.vista.wait('LABORATORY TEST NAME'))
        self.vista.write('')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('Select OPTION:'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.writectrl(chr(27) + chr(27)) # ??
        self.assertTrue(self.vista.wait('>>'))

        # Enter VEDD via 3 argument form into file 100 and ask about the
        # Varible pointer field OBJECT OF ORDER
        self.vista.write('..VEDD 100 G')
        self.assertTrue(self.vista.wait('Select'))
        self.vista.write('P')
        self.vista.write('2')
        self.assertTrue(self.vista.wait('Select NUMBER of your choice'))
        self.vista.write('2')
        self.assertTrue(self.vista.wait('Select'))
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))


    def test_routineSearch(self):
        self.vista.write('..RSEARCH')
        try:
            self.vista.wait('All Routines?',TIMEOUT)
            self.vista.write('') # Cache only
        except:
            pass
        self.vista.wait('Routine:')
        self.vista.write('XV*')
        self.vista.wait('Routine:')
        self.vista.write('')
        self.vista.wait('SEARCH STRING')
        self.vista.write('MV1')
        self.vista.wait('SEARCH STRING')
        self.vista.write('')
        self.vista.wait('EXCLUDE STRING')
        self.vista.write('')
        self.assertTrue(self.vista.wait('8. MV1'))
        self.vista.write('^')
        try:
            self.vista.wait('All Routines?',TIMEOUT)
            self.vista.write('') # Cache only
        except:
            pass
        self.vista.wait('Routine:')
        self.vista.write('')
        self.assertTrue(self.vista.wait('>>'))

    def test_ZP(self):
        #ZPRINT
        self.vista.write('..ZP')
        self.assertTrue(self.vista.wait('Example'))
        self.assertTrue(self.vista.wait('>>'))

        self.vista.write('..ZP XV')
        self.vista.wait('NOUSER')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))


    def test_UserList(self):
        self.vista.write('..UL')
        self.assertTrue(self.vista.wait('U S E R   L I S T'))
        self.assertTrue(self.vista.wait('>>'))

    def test_FilemanTemplateDisplayers(self):
        self.vista.write('..FMTI')
        self.vista.wait('INPUT TEMPLATE')
        self.vista.write('XU KSP INIT')
        self.vista.wait('LIFETIME OF VERIFY CODE')
        self.vista.wait('INPUT TEMPLATE')
        self.vista.write('')
        self.assertTrue(self.vista.wait('>>'))

        self.vista.write('..FMTP')
        self.vista.wait('PRINT TEMPLATE')
        self.vista.write('XUSERINQ')
        self.vista.wait('CPRS TAB:TAB DESCRIPTION')
        self.vista.wait('PRINT TEMPLATE')
        self.vista.write('')
        self.assertTrue(self.vista.wait('>>'))

        self.vista.write('..FMTS')
        self.vista.wait('SORT TEMPLATE')
        self.vista.write('PSO INTERVENTIONS')
        self.vista.wait('User is asked range')
        self.vista.wait('SORT TEMPLATE')
        self.vista.write('')
        self.assertTrue(self.vista.wait('>>'))

    def test_FilemanHelp(self):
        self.vista.write('..FMC')
        self.vista.wait('CALLABLE ROUTINES')
        self.vista.write('')
        self.vista.wait('DDSFILE')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.writectrl(chr(27) + '[B') # Down arrow
        self.vista.writectrl(chr(27) + '[B') # Down arrow
        self.vista.writectrl(chr(27) + '[B') # Down arrow
        self.vista.writectrl(chr(27) + '[C') # Right arrow
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))

    def test_KernelHelp(self):
        self.vista.write('..LF')
        self.vista.wait('L I B R A R Y   F U N C T I O N S')
        self.vista.write('')
        self.vista.wait('DATE FUNCTIONS - XLFDT')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.vista.write('^') # Go back
        self.assertTrue(self.vista.wait('>>'))

    def test_notes(self):
        self.vista.write('..NOTES')
        self.vista.wait('V P E   P A R A M E T E R   P A S S I N G')
        self.vista.writectrl(chr(27) + chr(27)) # Go back
        self.assertTrue(self.vista.wait('>>'))

    def test_key(self):
        self.vista.write('..KEY')
        self.vista.wait('K E Y B O A R D   I N T E R P R E T E R')
        self.vista.writectrl(chr(27) + 'OP') # F1
        self.vista.wait('80')
        self.vista.write('')
        self.vista.writectrl('.')            # Just a dot
        self.vista.wait('46')
        self.vista.writectrl(chr(27) + '[C') # Right arrow
        self.vista.write('')
        self.assertTrue(self.vista.wait('>>'))

    def test_param(self):
        self.vista.write('..PARAM')
        self.vista.wait('V P E   S Y S T E M   P A R A M E T E R S')
        self.vista.wait('Select NUMBER')
        self.vista.write('?')
        self.vista.wait('Select NUMBER')
        self.vista.write('1')
        self.vista.wait('Select NUMBER')
        self.vista.write('2')
        self.vista.wait('Select NUMBER')
        self.vista.write('3')
        self.vista.wait('Enter TIME-OUT:')
        self.vista.write('')
        self.vista.wait('Select NUMBER')
        self.vista.write('4')
        self.vista.wait('ROUTINE')
        self.vista.write('KBANQWIK')
        self.vista.wait('Select NUMBER')
        self.vista.write('5')
        self.vista.wait('Select NUMBER')
        self.vista.write('6')
        self.vista.wait('SCREEN WIDTH')
        self.vista.write('80')
        self.vista.wait('Select NUMBER')
        self.vista.write('7')
        self.vista.wait('SCREEN LENGTH')
        self.vista.write('24')
        self.vista.wait('Select NUMBER')
        #
        # Reset the prompt
        self.vista.write('2')
        self.vista.wait('Select NUMBER')
        #
        # Disallow width < 80; length < 24 (new feature in 15.0)
        self.vista.write('6')
        self.vista.wait('SCREEN WIDTH')
        self.vista.write('79')
        self.vista.wait('(>=80 or 0)')
        self.vista.write('?')
        self.vista.wait('(>=80 or 0)')
        self.vista.write('80')
        self.vista.wait('Select NUMBER')
        self.vista.write('7')
        self.vista.wait('SCREEN LENGTH')
        self.vista.write('20')
        self.vista.wait('(>=24 or 0)')
        self.vista.write('?')
        self.vista.wait('(>=24 or 0)')
        self.vista.write('24')
        self.vista.wait('Select NUMBER')
        
        # Go back to Auto-width (new feature in 15.0)
        self.vista.write('6')
        self.vista.wait('SCREEN WIDTH')
        self.vista.write('0')
        self.vista.wait('Select NUMBER')
        self.vista.write('7')
        self.vista.wait('SCREEN LENGTH')
        self.vista.write('0')
        self.vista.wait('Select NUMBER')
        #
        #
        # Go back to prompt
        self.vista.write('')
        self.assertTrue(self.vista.wait('>>'))


    def test_ZD(self):
        self.vista.write('..ZD X')
        self.vista.wait('OK TO DELETE?')
        self.vista.write('Y')
        self.vista.wait('XVVSIZE')
        self.vista.wait('>>')

    def test_CLH(self):
        self.vista.write('..CLH')
        self.vista.wait('>>')

    def test_DIC(self):
        self.vista.write('..DIC')
        self.vista.wait('DIC Look-up Template')
        for range in (0,7):
            self.vista.writectrl(chr(8))
        self.vista.write('')
        self.vista.wait('>>')
        
    def test_purge(self):
        self.vista.write('..PUR')
        self.vista.wait('>>')
        self.vista.write('..PUR 7')
        self.vista.wait('>>')

    def test_QSAVE(self):
        self.vista.write('..QSAVE')
        self.vista.wait('Save/Restore User QWIKs')
        self.vista.write('1')
        self.vista.wait('ROUTINE')
        self.vista.write('KBANQWIK')
        self.vista.wait('I will save your QWIKs to routine ^KBANQWIK.')
        self.vista.write('Y')
        self.vista.wait('>>')

        self.vista.write('..QSAVE')
        self.vista.wait('Save/Restore User QWIKs')
        self.vista.write('2')
        self.vista.wait('ROUTINE')
        self.vista.write('KBANQWIK')
        self.vista.wait('BOX')
        self.vista.write('6')
        self.vista.wait('ID')
        self.vista.write('1')
        self.vista.wait('>>')

    def test_syntaxHighlighting(self):
        # Turn on Syntax Highlighting
        self.vista.write('..PARAM')  # Parameters
        self.vista.wait('Select NUMBER')
        self.vista.write('8')        # Turn on Syntax Highlighting
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('>>')

        # Now View a Routine in Color
        self.vista.write('..VRR XV')
        self.vista.wait('<ESC><ESC>=Quit')
        self.vista.writectrl(chr(27) + '[6~') # Page Down
        self.vista.writectrl(chr(27) + '[6~') # Page Down
        self.vista.writectrl(chr(27) + '[6~') # Page Down
        self.vista.writectrl(chr(27) + '[6~') # Page Down
        self.vista.writectrl(chr(27) + '[6~') # Page Down
        self.vista.wait('<> <> <>')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('>>')

        # Delete routine KBANTEST2
        self.vista.write('..ZR KBANTEST2')
        boo = self.vista.wait('OK TO DELETE?')
        self.assertEqual(boo,1)
        self.vista.write('Y')
        boo = self.vista.wait('Removed')
        self.assertEqual(boo,1)
        self.vista.wait('>>')

        # Now create the new routine KBANTEST2
        self.vista.write('..E')
        self.vista.wait('ROUTINE')
        self.vista.write('KBANTEST2')
        self.vista.wait('^KBANTEST2]')
        self.vista.write('')
        self.vista.write('KBANTEST2' + chr(9) + '; TEST ROUTINE')
        self.vista.wait('E')
        self.vista.write(chr(9) + 'D USEZERO^XVEMSU')
        self.vista.wait('U')
        self.vista.write(' W "HELLO VPE",!')
        self.vista.wait('!')
        self.vista.write(' QUIT')
        self.vista.wait('T')
        self.vista.writectrl('TAG1')
        self.vista.wait('1')
        for x in range(0,4):
             self.vista.writectrl(chr(127)) # Backspace bug in Cache in 15.1
        self.vista.write('TAG1' + chr(9) + '; TEST TAG')
        self.vista.wait('G')
        self.vista.write(chr(9) + 'N Z')
        self.vista.wait('Z')
        self.vista.write(' S Z=1')
        for x in range(0,81):
             self.vista.write(' S Z=1')
             self.vista.wait('=============')
        self.vista.write(' D USEZERO^XVEMSU')
        self.vista.wait('U')
        self.vista.write(' W "BYE VPE",!')
        self.vista.wait('!')
        self.vista.write(' QUIT')
        self.vista.wait('T')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel line
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.write('')
        self.vista.wait('saved to disk')
        self.vista.wait('>>')
        self.vista.write('D ^KBANTEST2')
        self.vista.wait('HELLO VPE')
        self.vista.wait('>>')

        # Now edit the colors for syntax highlighting
        # Change Tag to be Yellow Foreground
        self.vista.write('..PARAM')
        self.vista.wait('Select NUMBER')
        self.vista.write('9')        # Syntax highlighting colors
        self.vista.wait('Set colors for error regions')
        self.vista.write('3')
        self.vista.wait('Use <TAB> or the arrow keys')
        self.vista.write(chr(9))
        self.vista.wait('Cyan')
        self.vista.write('')
        self.vista.wait('BACKGROUND')
        self.vista.write('')
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('>>')

        # Test Bad Input
        self.vista.write('..PARAM')
        self.vista.wait('Select NUMBER')
        self.vista.write('9')        # Syntax highlighting colors
        self.vista.wait('Set colors for error regions')
        self.vista.write('boofoo')
        self.vista.wait('To edit a parameter, enter number of your choice')
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('>>')

        ## Test ESC-ESC to cancel change
        self.vista.write('..PARAM')
        self.vista.wait('Select NUMBER')
        self.vista.write('9')        # Syntax highlighting colors
        self.vista.wait('Set colors for error regions')
        self.vista.write('9')
        self.vista.wait('Use <TAB> or the arrow keys')
        self.vista.write(chr(9))
        self.vista.wait('Off')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel
        self.vista.wait('BACKGROUND')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('>>')

        # Now View routine in color
        self.vista.write('..VRR XVEMSY')
        self.vista.wait('<ESC><ESC>=Quit')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('>>')

        # Go back to parameters and reset
        self.vista.write('..PARAM')
        self.vista.wait('Select NUMBER')
        self.vista.write('9')        # Syntax highlighting colors
        self.vista.wait('Select NUMBER')
        self.vista.write('0')        # Reset
        self.vista.write('')
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('>>')

        # Now View routine in color (again, reset colors)
        self.vista.write('..VRR XVEMSY')
        self.vista.wait('<ESC><ESC>=Quit')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('>>')

        # Go back to parameters and turn off syntax highlighting
        self.vista.write('..PARAM')
        self.vista.wait('Select NUMBER')
        self.vista.write('8')        # Syntax highlighting colors
        self.vista.wait('Select NUMBER')
        self.vista.write('')
        self.vista.wait('>>')

        # Now View routine in color (again, no colors)
        self.vista.write('..VRR XVEMSY')
        self.vista.wait('<ESC><ESC>=Quit')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('>>')

    def test_ZSAVE_ZLINK_percent(self):
        self.vista.write('..ZR %ZZVPETEST %ZZVPETEST2')
        boo = self.vista.wait('OK TO DELETE?')
        self.assertEqual(boo,1)
        self.vista.write('Y')
        boo = self.vista.wait('Removed')
        self.assertEqual(boo,1)
        self.vista.wait('>>')

        self.vista.write('..E')
        self.vista.wait('ROUTINE')
        self.vista.write('%ZZVPETEST')
        self.vista.wait('^%ZZVPETEST]')
        self.vista.write('')
        self.vista.write('%ZZVPETEST' + chr(9) + '; TEST ROUTINE') # Line 1
        self.vista.wait('E')
        self.vista.write(' WRITE "HELLO VPE3",!')                  # Line 2
        self.vista.wait('!')
        self.vista.write(' D ^%ZZVPETEST2')                        # Line 3
        self.vista.wait('2')
        self.vista.write(' QUIT')                                  # Line 4
        self.vista.wait('T')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel line
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.write('')
        self.vista.wait('saved to disk')
        self.vista.wait('>>')
        self.vista.write('D ^%ZZVPETEST')
        self.vista.wait('HELLO VPE3')
        self.vista.wait('>>')

        self.vista.write('..E %ZZVPETEST')
        self.vista.wait('^%ZZVPETEST]')
        self.vista.writectrl(chr(27) + 'OS' + chr(27) + '[D') # F4 Left Arrow - Go to first line
        self.vista.writectrl(chr(27) + '[B') # Down arrow once ; go to second line
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + '[C') # F1 Right Arrow - Go to end of line
        for i in range(0,4):
            self.vista.writectrl(chr(8)) # backspace over 3",!
        self.vista.write('4",!')
        self.vista.wait('!')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel line
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.write('')
        self.vista.wait('saved to disk')
        self.vista.wait('>>')
        self.vista.write('D ^%ZZVPETEST')
        self.vista.wait('HELLO VPE4')
        self.vista.wait('>>')

        self.vista.write('..E %ZZVPETEST2')
        self.vista.wait('^%ZZVPETEST2]')
        self.vista.write('')
        self.vista.write('%ZZVPETEST2' + chr(9) + '; TEST ROUTINE') # Line 1
        self.vista.wait('E')
        self.vista.write(' WRITE "HELLO VPE5",!')                  # Line 2
        self.vista.wait('!')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel line
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.write('')
        self.vista.wait('saved to disk')
        self.vista.wait('>>')

        self.vista.write('..E %ZZVPETEST')
        self.vista.wait('^%ZZVPETEST]')
        self.vista.writectrl(chr(27) + 'OS' + chr(27) + '[D') # F4 Left Arrow - Go to first line
        self.vista.writectrl(chr(27) + '[B') # Down arrow once ; go to second line
        self.vista.writectrl(chr(27) + '[B') # Down arrow once ; go to third line # now on D ^%ZZVEPTEST2
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + '[D') # F1 Left Arrow - Go to beginning of line
        self.vista.writectrl(chr(27) + '[C') # Right arrow once; now on space
        self.vista.writectrl(chr(27) + '[C') # Right arrow once; now on ^
        self.vista.writectrl(chr(27) + 'R') # Branch to new routine
        self.vista.wait('^%ZZVPETEST2]')
        self.vista.writectrl(chr(27) + 'OS' + chr(27) + '[D') # F4 Left Arrow - Go to first line
        self.vista.writectrl(chr(27) + '[B') # Down arrow once ; go to second line
        self.vista.writectrl(chr(27) + 'OP' + chr(27) + '[C') # F1 Right Arrow - Go to end of line ; WRITE "HELLO VPE5",!
        for i in range(0,4):
            self.vista.writectrl(chr(8)) # backspace over 5",!
        self.vista.write('6",!')
        self.vista.wait('!')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel line
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Do you wish to save your changes?')
        self.vista.write('Y')
        self.vista.wait('Changes saved to disk...')
        self.vista.write('')
        self.vista.wait('^%ZZVPETEST]')
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.write('Q')
        self.vista.wait('Changes not saved.')
        self.vista.wait('>>')
        self.vista.write('D ^%ZZVPETEST2')
        self.vista.wait('HELLO VPE6')
        self.vista.wait('>>')

    def test_error_crash_message(self):
        self.vista.write('S XVSIMERR=1')
        self.vista.wait('>>')
        self.vista.write('..E KBANTEST2')
        self.vista.wait('https://github.com/shabiel/VPE/issues')
        self.vista.write('')
        self.vista.wait('>>')
        self.vista.write('K XVSIMERR')
        self.vista.wait('>>')

    def test_RL(self):
        self.vista.write('..RL')
        try:
            self.vista.wait('All Routines?',TIMEOUT)
            self.vista.write('') # Cache only
        except:
            pass
        self.vista.wait('Routine:')
        self.vista.write('XV*')
        self.vista.write('')
        self.vista.wait('Select [B]LOCK [L]IST or [#]LINES')
        self.vista.write('B')
        self.vista.wait('DEVICE')
        self.vista.write('0;P-OTHER;80;999999')
        self.vista.wait('to continue..')
        self.vista.write('')

        try:
            self.vista.wait('All Routines?',TIMEOUT)
            self.vista.write('') # Cache only
        except:
            pass
        self.vista.wait('Routine:')
        self.vista.write('XV*')
        self.vista.write('')
        self.vista.wait('Select [B]LOCK [L]IST or [#]LINES')
        self.vista.write('L')
        self.vista.wait('DEVICE')
        self.vista.write('0;P-OTHER;80;999999')
        self.vista.wait('to continue..')
        self.vista.write('')

        try:
            self.vista.wait('All Routines?',TIMEOUT)
            self.vista.write('') # Cache only
        except:
            pass
        self.vista.wait('Routine:')
        self.vista.write('XV*')
        self.vista.write('')
        self.vista.wait('Select [B]LOCK [L]IST or [#]LINES')
        self.vista.write('3')
        self.vista.wait('DEVICE')
        self.vista.write('0;P-OTHER;80;999999')
        self.vista.wait('to continue..')
        self.vista.write('')

        try:
            self.vista.wait('All Routines?',TIMEOUT)
            self.vista.write('') # Cache only
        except:
            pass
        self.vista.wait('Routine:')
        self.vista.write('')
        self.vista.wait('>>')
        
    def zztest_lotsOfLines(self): # Commented out as takes too long to run
        # Delete routine KBANTEST3
        self.vista.write('..ZR KBANTEST3')
        boo = self.vista.wait('OK TO DELETE?')
        self.assertEqual(boo,1)
        self.vista.write('Y')
        boo = self.vista.wait('Removed')
        self.assertEqual(boo,1)
        self.vista.wait('>>')

        # Now create the new routine KBANTEST3
        self.vista.write('..E')
        self.vista.wait('ROUTINE')
        self.vista.write('KBANTEST3')
        self.vista.wait('^KBANTEST3]')
        self.vista.write('')
        self.vista.write('KBANTEST3' + chr(9) + '; TEST ROUTINE')
        self.vista.wait('E')
        self.vista.write(chr(9) + 'N Z')
        self.vista.wait('Z')
        for x in range(0,1001):
             self.vista.write(' S Z=1')
             self.vista.wait('=============')
        self.vista.write(' QUIT')
        self.vista.wait('T')
        self.vista.writectrl(chr(27) + chr(27)) # Cancel line
        self.vista.writectrl(chr(27) + chr(27)) # Exit
        self.vista.wait('Save your changes?')
        self.vista.write('')
        self.vista.wait('saved to disk')
        self.vista.wait('>>')

    def test_stopVPE(self):
        self.vista.write('HALT')
        self.vista.wait('>')

    def test_upgradeVPE(self):
        self.vista.write('D UPGRADE^XV')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('to continue')
        self.vista.write('')
        self.vista.wait('Load VPE Shell global')
        self.vista.write('Y')
        self.vista.wait('to continue..')
        self.vista.write('')
        self.assertEqual(self.vista.wait('>'),1)

    def test_reEnterVPE(self):
        self.vista.write('D ^XV')
        self.vista.wait('>>')

    def test_editorErrorTrap(self):
        self.vista.write('S XVSIMERR3=1')
        self.vista.wait('>>')
        self.vista.write('..VRR XV')
        self.vista.wait('https://github.com/shabiel/VPE/issues')
        self.vista.write('')
        self.vista.wait('>>')

    def test_stopVPE2(self):
        self.vista.write('HALT')
        self.vista.wait('>')


if __name__ == '__main__':
    # OSEHRA Testing Framework Setup
    test_suite_driver = TestHelper.TestSuiteDriver(__file__)
    test_suite_details = test_suite_driver.generate_test_suite_details()
    test_suite_details.coverage_subset = ['XV*']
    test_suite_driver.pre_test_suite_run(test_suite_details)
    test_driver = TestHelper.TestDriver("VPE.out")

    # Python Unit Testing setup
    del sys.argv[1:]  # don't pass the arguments down to the unit tester

    # Next stanza: run tests in order of declaration, top to bottom.
    loader = unittest.TestLoader()
    if   sys.version_info[0] == 2: ln = lambda f: getattr(VPEUnitTests, f).im_func.func_code.co_firstlineno
    else                         : ln = lambda f: getattr(VPEUnitTests, f).__code__.co_firstlineno
    lncmp = lambda a, b: (ln(a) > ln(b)) - (ln(a) < ln(b))
    loader.sortTestMethodsUsing = lncmp

    # Turn on profiling
    #pr = cProfile.Profile()
    #pr.enable()

    # Run the main code
    unittest.main(testLoader=loader, verbosity=2, exit=False)

    # Disable profiling
    #pr.disable()

    # Print stats
    #ps = pstats.Stats(pr).sort_stats('cumulative')
    #ps.print_stats()

#---------------------------------------------------------------------------
# Copyright 2017,2019 Sam Habiel
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

