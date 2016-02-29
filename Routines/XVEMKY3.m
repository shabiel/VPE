XVEMKY3 ;DJB,KRN**Screen Variables ; 9/8/02 6:20pm
 ;;13.0;VICTORY PROG ENVIRONMENT;;Feb 29, 2016
 ;
BLANK ;
 D BLANK1,BLANK2,BLANK3,BLANK4
 Q
BLANK1 ;Blank - cursor to end-of-screen
 Q:$D(XVVS("BLANK_C_EOS"))
 I $G(IOST(0))]"",$D(^%ZIS(2,IOST(0),5)),$P(^(5),"^",7)]"" S XVVS("BLANK_C_EOS")=$P(^(5),"^",7) Q
 S XVVS("BLANK_C_EOS")="$C(27)_""[J"""
 Q
BLANK2 ;Blank - top-of-screen to cursor
 Q:$D(XVVS("BLANK_TOS_C"))
 I $G(IOST(0))]"",$D(^%ZIS(2,IOST(0),13)),$P(^(13),"^",1)]"" S XVVS("BLANK_TOS_C")=$P(^(13),"^",1) Q
 S XVVS("BLANK_TOS_C")="$C(27)_""[1J"""
 Q
BLANK3 ;Blank - cursor to end-of-line
 Q:$D(XVVS("BLANK_C_EOL"))
 I $G(IOST(0))]"",$D(^%ZIS(2,IOST(0),5)),$P(^(5),"^",6)]"" S XVVS("BLANK_C_EOL")=$P(^(5),"^",6) Q
 S XVVS("BLANK_C_EOL")="$C(27)_""[K"""
 Q
BLANK4 ;Blank - start-of-line to cursor
 Q:$D(XVVS("BLANK_SOL_C"))
 I $G(IOST(0))]"",$D(^%ZIS(2,IOST(0),13)),$P(^(13),"^",3)]"" S XVVS("BLANK_SOL_C")=$P(^(13),"^",3) Q
 S XVVS("BLANK_SOL_C")="$C(27)_""[1K"""
 Q
 ;====================================================================
ZSAVE ;Set up XVVS("ZS") to zsave a routine.
 ;
 I $D(^DD("OS",XVV("OS"),"ZS")) S XVVS("ZS")=^("ZS") Q:XVVS("ZS")]""
 I $D(^DD("OS")),'$D(^DD("OS",XVV("OS"),"ZS")) S FLAGQ=1 D  Q
 . W $C(7),!!?5,"Your Mumps system has no way to ZSAVE a routine. I'm aborting.",!!
 ;
 ;DSM,MSM,DSM for Open VMS
 I ",2,8,16,"[(","_XVV("OS")_",") D  Q
 . S XVVS("ZS")="NEW %Y ZR  S %Y=0 X ""F  S %Y=$O(^UTILITY($J,0,%Y)) Q:%Y'>0  ZI ^(%Y)"" ZS @X"
 ;
 ;DTM
 I XVV("OS")=9 D  Q
 . S XVVS("ZS")="NEW %X,%Y S %X="""",%Y=0 X ""F  S %Y=$O(^UTILITY($J,0,%Y)) Q:%Y'>0  S %X=%X_$C(10)_^(%Y)"" ZS @X:$E(%X,2,999999)"
 ;
 ;CACHE
 I XVV("OS")=18 D  Q
 . S XVVS("ZS")="NEW %Y ZR  S %Y=0 X ""F  S %Y=$O(^UTILITY($J,0,%Y)) Q:%Y'>0  Q:'$D(^(%Y))  ZI ^(%Y)"" ZS @X"
 ;
 ;-> GTM
 I XVV("OS")=17 D  Q
 . S XVVS("ZS")="N %I,%F,%S S %I=$I,%F=$P($ZRO,"","")_X_"".m"" O %F:(NEWVERSION) U %F X ""S %S=0 F  S %S=$O(^UTILITY($J,0,%S)) Q:%S=""""""""  Q:'$D(^(%S))  S %=^UTILITY($J,0,%S) I $E(%)'="""";"""" W %,!"" C %F U %I"
 ;
 I XVV("OS")=19 D  Q
 . S XVVS("ZS")="N %I,%F,%S S %I=$I,%F=$P($ZRO,"" "")_""/""_$TR(X,""%"",""_"")_"".m"" O %F:(NEWVERSION) U %F X ""S %S=0  F  S %S=$O(^UTILITY($J,0,%S)) Q:%S=""""""""  Q:'$D(^(%S))  "
 . S XVVS("ZS")=XVVS("ZS")_"S %=^UTILITY($J,0,%S) I $E(%)'="""";"""" W %,!"" C %F U %I"
 ;
 ;-> Abort if no XVVS("ZS")
 D ZSAVEMSG S FLAGQ=1
 Q
ZSAVEMSG ;Can't ZSAVE a routine
 W $C(7),!!?5,"You don't have VA Fileman in this UCI, and I don't know how to"
 W !?5,"ZSAVE a routine on your Mumps system. I'm aborting."
 W !!?5,"Review subroutine ZSAVE^XVEMKY3. You may edit this routine and"
 W !?5,"add code to cover your M system. If you are running VA Fileman,"
 W !?5,"see ^DD(""OS"",system#,""ZS"") for your M system.",!!
 Q
