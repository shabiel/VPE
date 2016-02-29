XVEMSU2 ;DJB,VSHL**Utilities - ZPrint,ZRemove,Version ; 9/7/02 1:55pm
 ;;13.0;VICTORY PROG ENVIRONMENT;;Feb 29, 2016
 ;
ZPRINT ;ZP System QWIK to print a routine
 I $G(%1)']"" D ZPMSG Q
 D RTN^XVEMKT(%1)
 Q
ZPMSG ;No parameter passed
 W $C(7),!!,"..ZP will print a routine to your screen in scrolling mode. Pass the name"
 W !,"of the routine you want to print, as a parameter."
 W !!,"Example: ..ZP %ZIS     Print routine ^%ZIS",!
 Q
 ;====================================================================
ZREMOVE() ;Delete a routine
 I $G(%1)']"" D ZRMSG Q 0
 NEW CHK,I,TMP
 S CHK=0 F I=1:1:9 S TMP="%"_I I $G(@TMP)]"",@TMP["^" S CHK=1
 I CHK W $C(7),!,"..ZR parameters should not contain ""^"".",! Q 0
 I $$YN^XVEMKU1("OK TO DELETE? ",2)'=1 Q 0
 Q 1
ZRMSG ;
 W $C(7),!!,"..ZR will delete from 1 to 9 routines. You pass the names of the routines"
 W !,"to be deleted, as parameters."
 W !!,"Ex 1: ..ZR RTN1             Delete routine ^RTN1"
 W !!,"Ex 2: ..ZR RTN1 RTN2 RTN3   Delete routines ^RTN1,^RTN2, & ^RTN3.",!
 Q
 ;====================================================================
VERSION ;VShell Version Information
 D:'$D(XVV("RON")) REVVID^XVEMKY2
 W !?3,@XVV("RON")
 W " VPE version ",$P($T(+2),";",3)," "
 W @XVV("ROFF"),!
 Q
 ;
CACHE ;
 NEW XVVS,VRRPGM,VRRS
 S VRRS=1
 KILL ^TMP("XVV","IR"_VRRS,$J)
 S VRRS=1
 D ZSAVE^XVEMKY3 Q:FLAGQ
 F VRRPGM="XVEMKRN","XVEMSU1" D  ;
 . D SETGLB^XVEMRS1
 . D CONVERT^XVEMRV(VRRS)
 . X ^XVEMS("E",2)
 KILL ^TMP("XVV","IR"_VRRS,$J)
 KILL ^TMP("XVV","VRR",$J)
 Q
