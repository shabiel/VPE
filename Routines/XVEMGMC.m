XVEMGMC ;DJB,VGL**Check FM, Check Node [6/14/95 10:39pm]
 ;;13.0;VICTORY PROG ENVIRONMENT;;Feb 29, 2016
 ;
GOTO ;Goto line number
 NEW ND,X
 S ND=$$GETREF^XVEMKTR("IG"_GLS) Q:ND="^"
 I ND="***" W $C(7) Q
 I '$D(^TMP("XVV","VGL"_GLS,$J,ND)) D  Q:ND'>0
 . S ND=$O(^TMP("XVV","VGL"_GLS,$J,ND)) Q:ND>0
 . S ND=$O(^TMP("XVV","VGL"_GLS,$J,ND),-1)
 S XVVT("TOP")=$$GETSCR^XVEMKTR(ND,"IG"_GLS)
 S XVVT("HLN")=XVVT("TOP")+1
 Q
CHECKFM() ;;0=Fileman not present  1=Fileman
 I $D(^DD),$D(^DIC) Q 1
 D MSG^XVEMGUM(18,1)
 Q 0
CHKNODE ;Do not display Xref or Zero nodes
 I SUBNUM="Y" D  Q:FLAGQ
 . I $P(SUBCHK,ZDELIM,2)=0,$L(SUBCHK,ZDELIM)>2 D MSG^XVEMGUM(2,1) S FLAGQ=1  Q
 . F I=2:2:$L(SUBCHK,ZDELIM) I +$P(SUBCHK,ZDELIM,I)'=$P(SUBCHK,ZDELIM,I) D  Q
 . . I $P(SUBCHK,ZDELIM,I)["%" D MSG^XVEMGUM(15,1) S FLAGQ=1 Q
 . . S FLAG="XREF",FLAGXREF=I ;Marks a Xref node
 I SUBNUM="Y",FLAG'="XREF",$L(SUBCHK,ZDELIM)#2=0 S FLAG="ZERO"
 I SUBNUM="N" D  Q:FLAGQ
 . I $P(SUBCHK,ZDELIM)=0,$L(SUBCHK,ZDELIM)>1 D MSG^XVEMGUM(2,1) S FLAGQ=1 Q
 . F I=1:2:$L(SUBCHK,ZDELIM) I +$P(SUBCHK,ZDELIM,I)'=$P(SUBCHK,ZDELIM,I) D  Q
 . . I $P(SUBCHK,ZDELIM,I)["%" D MSG^XVEMGUM(15,1) S FLAGQ=1 Q
 . . S FLAG="XREF",FLAGXREF=I ;Marks a Xref node
 I SUBNUM="N",FLAG'="XREF",$L(SUBCHK,ZDELIM)#2 S FLAG="ZERO"
 I SUBNUM="DIC" D MSG^XVEMGUM(16,1) S FLAGQ=1 Q
 Q:FLAG="XREF"!(FLAG="ZERO")
 ;Verify zero node and check for Word Processing field.
 S TEMP="" I $L(SUBCHK,ZDELIM)>2 F I=1:1:$L(SUBCHK,ZDELIM)-2 S TEMP=TEMP_$P(SUBCHK,ZDELIM,I)_","
 S TEMP=GL_"("_TEMP_"0)" I '$D(@TEMP)#2 D MSG^XVEMGUM(17,1) S FLAGQ=1 Q
 S TEMP1=$P(@TEMP,U,2),XVVX="" F I=1:1:$L(TEMP1) I $E(TEMP1,I)?1N!($E(TEMP1,I)?1".") S XVVX=XVVX_$E(TEMP1,I) ;Strip off alpha
 I XVVX!($L(SUBCHK,ZDELIM)<4) Q
 S TEMP="" F I=1:1:($L(SUBCHK,ZDELIM)-4) S TEMP=TEMP_$P(SUBCHK,ZDELIM,I)_","
 S TEMP=GL_"("_TEMP_"0)" I '$D(@TEMP)#2 D MSG^XVEMGUM(17,1) S FLAGQ=1 Q
 S XVVX=$P(@TEMP,U,2),XVVY="" F I=1:1:$L(XVVX) I $E(XVVX,I)?1N!($E(XVVX,I)?1".") S XVVY=XVVY_$E(XVVX,I) ;Strip off alpha
 I XVVX']""!(XVVY']"") D MSG^XVEMGUM(17,1) S FLAGQ=1 Q
 S FLAG="WP"
 Q
