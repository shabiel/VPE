XVEMSF ;DJB,VSHL**FM Calls [3/6/96 6:16pm]
 ;;13.0;VICTORY PROG ENVIRONMENT;;Feb 29, 2016
 ;
EN ;Entry Point
 NEW CNT,COL,COLUMNS,COLCNT,HD,LAST,PROMPT,SET,SPACES,WIDTH,WRITE
 NEW CNTOLD,DX,DY,FLAGQ,I,OPT,TEST,TXT,XVVS,X,Y
 I '$D(XVV("OS")) NEW XVV
 S FLAGQ=0 D INIT Q:FLAGQ
 X XVVS("RM0")
TOP ;
 F  S FLAGQ=0 D HD^XVEMSHY,LIST,GETOPT Q:FLAGQ  D RUN Q:FLAGQ
EX ;
 X XVVS("RM0") W @XVV("IOF")
 Q
GETOPT ;
 X PROMPT S OPT=$$READ^XVEMKRN()
 I OPT="^" S FLAGQ=1 Q
 I ",<ESC>,<F1E>,<F1Q>,<TAB>,<TO>,"[(","_XVV("K")_",") S FLAGQ=1 Q
 I XVV("K")="<RET>" S OPT=CNT Q
 I XVV("K")?1"<A"1A1">" S CNTOLD=CNT D ARROW S OPT=CNT D REDRAW G GETOPT
 S OPT=$$ALLCAPS^XVEMKU(OPT),TEST=0 D  I TEST Q
 . F I=1:1 S X=$P($T(MENU+I),";",5) Q:X=""  I $E(X,1,$L(OPT))=OPT S (CNT,OPT)=I,COL=$P($T(MENU+I),";",3),TEST=1 Q
 G GETOPT
ARROW ;Arrow Keys
 I "<AU>,<AD>"[XVV("K") D  S COL=$P($T(MENU+CNT),";",3) Q
 . I XVV("K")="<AU>" S CNT=CNT-1 S:CNT<1 CNT=LAST Q
 . I XVV("K")="<AD>" S CNT=CNT+1 S:CNT>LAST CNT=1
 I XVV("K")="<AR>" Q:COL=COLCNT  D  D ADJUST Q
 . S CNT=CNT+COL(COL),COL=COL+1 S:CNT>LAST CNT=LAST
 I XVV("K")="<AL>" Q:COL=1  D  D ADJUST Q
 . S COL=COL-1,CNT=CNT-COL(COL)
 Q
RUN ;Run selected routine
 S X=$P($T(MENU+OPT),";",6) I X="QUIT" S FLAGQ=1 Q
 NEW CNT,COL,COLUMNS,COLCNT,HD,LAST,PROMPT,SET,SPACES,WIDTH,WRITE
 I X]"" W @XVV("IOF") D @X X XVVS("RM0")
 Q
LIST ;List Menu Options
 F I=1:1 S TXT=$T(MENU+I) Q:TXT=""!(TXT[";***")   X SET,WRITE
 S TXT=$T(MENU+CNT) Q:TXT=""
 X SET W @XVV("RON") X WRITE W @XVV("ROFF")
 Q
REDRAW ;User moved cursor
 S TXT=$T(MENU+CNTOLD) X SET,WRITE
 S TXT=$T(MENU+CNT) X SET W @XVV("RON") X WRITE W @XVV("ROFF")
 Q
ADJUST ;Adjust CNT when you switch columns.
 F  Q:$P($T(MENU+CNT),";",3)=COL  S CNT=CNT-1
 Q
INIT ;Initialize variables
 S COLUMNS="18^18",WIDTH=33
 S HD="FILEMAN 20 - CALLABLE ROUTINES"
 D INIT^XVEMSHY
 S PROMPT="S DX=3,DY=22 X XVVS(""CRSR"") W ""SELECT: "",@XVVS(""BLANK_C_EOL"")"
 Q
MENU ;MENU OPTIONS
 ;;1;DDS...ScreenMan;DDS;HELP^XVEMKT("DDS");2;3
 ;;1;DDIOL.Writer;DDIOL;HELP^XVEMKT("DDIOL");2;4
 ;;1;DIAC..File access;DIAC;HELP^XVEMKT("DIAC");2;5
 ;;1;DIAXU.Extract data;DIAXU;HELP^XVEMKT("DIAXU");2;6
 ;;1;DIB...User controlled edit;DIB;HELP^XVEMKT("DIB");2;7
 ;;1;DIC...Look-up.Add;DIC;HELP^XVEMKT("DIC");2;8
 ;;1;DIC1..Custom look-up.File info;DIC1;HELP^XVEMKT("DIC1");2;9
 ;;1;DICD..Wait msg;DICD;HELP^XVEMKT("DICD");2;10
 ;;1;DICN..New entry.YES/NO;DICN;HELP^XVEMKT("DICN");2;11
 ;;1;DICQ..Look-up display;DICQ;HELP^XVEMKT("DICQ");2;12
 ;;1;DICRW.Required variables;DICRW;HELP^XVEMKT("DICRW");2;13
 ;;1;DID...DD list;DID;HELP^XVEMKT("DID");2;14
 ;;1;DIE...Edit;DIE;HELP^XVEMKT("DIE");2;15
 ;;1;DIEZ..Input temp compile;DIEZ;HELP^XVEMKT("DIEZ");2;16
 ;;1;*DIFG.Filegrams;*DIFG;HELP^XVEMKT("DIFG");2;17
 ;;1;DIK...Delete.Reindex;DIK;HELP^XVEMKT("DIK");2;18
 ;;1;DIKZ..Xref compile;DIKZ;HELP^XVEMKT("DIKZ");2;19
 ;;1;DIM...Code validate;DIM;HELP^XVEMKT("DIM");2;20
 ;;2;DIO2..Intern to extern DATE;DIO2;HELP^XVEMKT("DIO2");40;3
 ;;2;DIP...Print;DIP;HELP^XVEMKT("DIP");40;4
 ;;2;DIPT..Print/Sort Temp;DIPT;HELP^XVEMKT("DIPT");40;5
 ;;2;DIPZ..Print Temp Compile;DIPZ;HELP^XVEMKT("DIPZ");40;6
 ;;2;DIQ...Data display.DATE conver;DIQ;HELP^XVEMKT("DIQ");40;7
 ;;2;DIQ1..Data retrieve;DIQ1;HELP^XVEMKT("DIQ1");40;8
 ;;2;*DIR..Reader;*DIR;HELP^XVEMKT("DIR");40;9
 ;;2;DIS...Search;DIS;HELP^XVEMKT("DIS");40;10
 ;;2;DIU2..DD delete;DIU2;HELP^XVEMKT("DIU2");40;11
 ;;2;DIWE..Text edit;DIWE;HELP^XVEMKT("DIWE");40;12
 ;;2;DIWF..Form document;DIWF;HELP^XVEMKT("DIWF");40;13
 ;;2;DIWP..Word process.;DIWP;HELP^XVEMKT("DIWP");40;14
 ;;2;DIWW..Output last line;DIWW;HELP^XVEMKT("DIWW");40;15
 ;;2;%DT...DATE/Time input/convert;%DT;HELP^XVEMKT("%DT");40;16
 ;;2;%DTC..DATE/Time manipulate;%DTC;HELP^XVEMKT("%DTC");40;17
 ;;2;COMMA.%DTC Number format;COMMA;HELP^XVEMKT("COMMA");40;18
 ;;2;%RCR..Array move;%RCR;HELP^XVEMKT("%RCR");40;19
 ;;2;Quit;QUIT;QUIT;40;20
