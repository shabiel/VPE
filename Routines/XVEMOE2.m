XVEMOE2 ;DJB,VRROLD**BREAK,JOIN [12/31/94]
 ;;13.0;VICTORY PROG ENVIRONMENT;;Feb 29, 2016
 ;
BREAK ;Break a line
 NEW BRK,CD,DX,DY,FLAGQ,VRRLN,X1,X2
 S FLAGQ=0 D BOTTOM^XVEMOU,BRKLINE G:FLAGQ BRKEX D BRKTOP
BRKEX ;Exit
 Q
BRKLINE ;Get line
 S VRRLN=$$GETLINE^XVEMOU("BREAK WHICH LINE NUMBER: ")
 I VRRLN="^" S FLAGQ=1 Q
 I VRRLN'?1.N D MSG2^XVEMOUM(14) G BRKLINE
 S CD=^TMP("XVV","VRR",$J,VRRS,"TXT",VRRLN)
 Q
BRKTOP ;Process break
 D BOTTOM^XVEMOU S DX=0,DY=0 X XVVS("XY")
 W "*",CD
BRKTOP1 ;
 W !?1,"BREAK AFTER WHAT CODE: "
 R BRK:XVV("TIME") S:'$T BRK="^" I "^"[BRK Q
 I "??"[BRK D  G BRKTOP1
 . W !?1,"The line will be broken AFTER the code you enter"
 I CD'[BRK D  G BRKTOP1
 . W $C(7),"   No match"
 S X1=$E(CD,1,($F(CD,BRK)-1)),X2=$E(CD,$F(CD,BRK),999)
 I $L(X1,$C(9))'=2 D  G BRKTOP1
 . W $C(7),"   You may not break at a line tag"
 I X2']"" W $C(7),"   Invalid entry" G BRKTOP1
 F  Q:$E(X1,$L(X1))'=" "  S X1=$E(X1,1,($L(X1)-1))
 F  Q:$E(X2)=""!($E(X2)'=" ")  S X2=$E(X2,2,999)
 S X2=$C(9)_X2
 S ^TMP("XVV","VRR",$J,VRRS,"TXT",VRRLN)=X1
 S VRRHIGH=VRRHIGH+1
 S $P(^TMP("XVV","VRR",$J,VRRS,"HOT"),"^",1)=VRRHIGH
 F I=VRRHIGH:-1:(VRRLN+2) S ^TMP("XVV","VRR",$J,VRRS,"TXT",I)=^TMP("XVV","VRR",$J,VRRS,"TXT",(I-1))
 S ^TMP("XVV","VRR",$J,VRRS,"TXT",(VRRLN+1))=X2,VRRLN=VRRLN+1,FLAGSAVE=1
 Q
JOIN ;Join 2 lines
 NEW I,LN1,LN1CD,LN2,LN2CD
 D BOTTOM^XVEMOU
JOINA S LN1=$$GETLINE^XVEMOU("1ST LINE NUMBER: ") Q:LN1="^"
 I LN1'?1.N D MSG2^XVEMOUM(14) G JOINA
JOIN1 D BOTTOM1^XVEMOU
 S LN2=$$GETLINE^XVEMOU("2ND LINE NUMBER: ") Q:LN2="^"
 I LN2'?1.N D MSGS^XVEMOUM(14,1) G JOIN1
 I LN1=LN2 D MSGS^XVEMOUM(18,1) G JOIN1
 S LN1CD=^TMP("XVV","VRR",$J,VRRS,"TXT",LN1)
 S LN2CD=$P(^TMP("XVV","VRR",$J,VRRS,"TXT",LN2),$C(9),2,999) ;Strip off any line tag
 I ($L(LN1CD)+$L(LN2CD))>245 D MSGS^XVEMOUM(19,1) G JOIN1
 S ^TMP("XVV","VRR",$J,VRRS,"TXT",LN1)=LN1CD_" "_LN2CD ;Insert a space
 ;Delete 2nd line
 F I=LN2:1:(VRRHIGH-1) S ^TMP("XVV","VRR",$J,VRRS,"TXT",I)=^TMP("XVV","VRR",$J,VRRS,"TXT",(I+1))
 KILL ^TMP("XVV","VRR",$J,VRRS,"TXT",VRRHIGH)
 S VRRHIGH=VRRHIGH-1,FLAGSAVE=1
 S $P(^TMP("XVV","VRR",$J,VRRS,"HOT"),"^",1)=VRRHIGH
 Q
