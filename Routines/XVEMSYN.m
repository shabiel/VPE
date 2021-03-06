XVEMSYN ;V4W/DLW - Syntax highlighting ;2019-08-09  4:31 PM
 ;;15.2;VICTORY PROG ENVIRONMENT;;Aug 27, 2019
 ; (c) David Wicksell 2019
 ;
SYNTAX(XVBUFFER,XVBUFNUM,XVW) ;Build a syntax structure for a corresponding line
 N XVCHAR,XVUCHAR,XVDATA,XVEXT,XVFLAG
 S XVBUFNUM=$G(XVBUFNUM)
 S XVW=$G(XVW,1)
 I XVW=0 S XVW=$L(XVBUFFER)+1
 S XVFLAG=0
 I $E(XVW,1)="+" S XVFLAG=1,$E(XVW,1)=""
 I $E(XVW,1)="-" S XVFLAG=2,$E(XVW,1)=""
 S (XVDATA("ARG"),XVDATA("FUNC"),XVDATA("PAT"),XVDATA("STRING"),XVDATA("TAG"),XVDATA,XVEXT)=0
 S (XVDATA("CMD"),XVDATA("STATE"),XVDATA("IDX"))=""
 W:XVW $$CONTROL("DEF")
 I XVBUFFER=" <> <> <>" W:XVW XVBUFFER Q
 I XVBUFNUM,$G(^TMP("XVV","IR"_VRRS,$J,XVBUFNUM+1),$C(30))'[$C(30),^(XVBUFNUM+1)'=" <> <> <>" D
 . I $D(^TMP("XVV","IR"_VRRS,$J,XVBUFNUM+1,"STATE")) K ^("STATE")
 . S XVEXT=1
 I $E(XVBUFFER,1)=" ",XVBUFFER'[$C(30) D
 . N XVSTATE
 . M XVDATA=^TMP("XVV","IR"_VRRS,$J,XVBUFNUM,"STATE")
 . S XVSTATE=XVDATA("STATE")
 . I XVSTATE="" W:XVW $P(XVBUFFER,$C(30),1),$P(XVBUFFER,$C(30),2) Q
 . W:'XVFLAG&(XVDATA'<XVW) $E(XVBUFFER,1,9)
 . I XVSTATE="ERROR" W:XVDATA'<XVW $$CONTROL("ERR")
 . I XVSTATE="COMMENT" W:XVDATA'<XVW $$CONTROL("COM")
 . I XVSTATE="TAG" W:XVDATA'<XVW $$CONTROL("TAG")
 . I XVSTATE="COMMAND" W:XVDATA'<XVW $$CONTROL("CMD")
 . I XVSTATE="ARGUMENT" W:XVDATA'<XVW $$CONTROL("ARG")
 . I XVSTATE="FUNCTION" W:XVDATA'<XVW $$CONTROL("FUNC")
 . I XVSTATE="PUNCMARK" W:XVDATA'<XVW $$CONTROL("PUNC")
 . I XVSTATE="NUMBER" W:XVDATA'<XVW $$CONTROL("NUM")
 . I XVSTATE="STRING" W:XVDATA'<XVW $$CONTROL("STR")
 . S XVDATA=9
 . G @XVSTATE
 E  D
 . I XVFLAG=1 N XVTAGL S XVTAGL=$L($P(XVBUFFER,$C(30),1))+1 W:XVW'>XVTAGL " "
 . D START(XVBUFFER,.XVDATA)
 I XVEXT M ^TMP("XVV","IR"_VRRS,$J,XVBUFNUM+1,"STATE")=XVDATA
 E  K ^TMP("XVV","IR"_VRRS,$J,XVBUFNUM+1,"STATE")
 W:XVW $$CONTROL("DEF")
 S $X=$S($L(XVBUFFER)<1:0,1:$L(XVBUFFER)-1)
 Q
 ;
START(XVBUFFER,XVDATA) ;Start state
 S XVDATA=1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" Q
 I XVBUFFER[$C(30),+XVBUFFER'>VRRHIGH,XVCHAR?1N W:XVDATA'<XVW XVCHAR G STATUS
 I XVCHAR?1(1A,1"%") S XVDATA("TAG")=1 W:XVDATA'<XVW $$CONTROL("TAG"),XVCHAR G TAG
 I XVCHAR?1N S XVDATA("TAG")=2 W:XVDATA'<XVW $$CONTROL("TAG"),XVCHAR G TAG
 I XVCHAR=" "!(XVCHAR=$C(9)) W:XVDATA'<XVW $$CONTROL("TAG"),XVCHAR G TAG
 I XVCHAR=$C(30) W:XVDATA'<XVW $$CONTROL("CMD") G COMMAND
 I XVCHAR=";" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
STATUS ;Status state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" Q
 I XVCHAR?1N W:XVDATA'<XVW XVCHAR G STATUS
 I XVCHAR=" "!(XVCHAR=$C(9)) W:XVDATA'<XVW XVCHAR G STATUS
 I XVCHAR?1(1A,1"%") W:XVDATA'<XVW $$CONTROL("TAG"),XVCHAR G TAG
 I XVCHAR=$C(30) W:XVDATA'<XVW $$CONTROL("CMD") G COMMAND
 I XVCHAR=";" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
TAG ;Tag state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="TAG" Q
 I XVDATA("TAG")=0,XVCHAR="%" S XVDATA("TAG")=1 W:XVFLAG $$CONTROL("TAG") W:XVDATA'<XVW XVCHAR G TAG
 I XVDATA("TAG")=0,XVCHAR?1N S XVDATA("TAG")=2 W:XVFLAG $$CONTROL("TAG") W:XVDATA'<XVW XVCHAR G TAG
 I XVDATA("TAG")<2,XVCHAR?1A S XVDATA("TAG")=1 W:XVFLAG $$CONTROL("TAG") W:XVDATA'<XVW XVCHAR G TAG
 I XVCHAR?1N W:XVDATA'<XVW XVCHAR G TAG
 I XVCHAR=" "!(XVCHAR=$C(9)) S XVDATA("TAG")=0 W:XVFLAG $$CONTROL("TAG") W:XVDATA'<XVW XVCHAR G TAG
 I XVCHAR?1(1":",1"(") S XVDATA("CMD")="TAG",XVDATA("TAG")=0  W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 I XVCHAR=$C(30) S XVDATA("TAG")=0 W:XVDATA'<XVW $$CONTROL("CMD") G COMMAND
 I XVCHAR=";" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
ERROR ;Error state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="ERROR" Q
 W:XVFLAG $$CONTROL("ERR") W:XVDATA'<XVW XVCHAR G ERROR
 Q
 ;
COMMENT ;Comment state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="COMMENT" Q
 W:XVFLAG $$CONTROL("COM") W:XVDATA'<XVW XVCHAR G COMMENT
 Q
 ;
COMMAND ;Command state
 S XVDATA=XVDATA+1
 S XVUCHAR=$$ALLCAPS^XVEMKU($E(XVBUFFER,XVDATA))
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT=1 XVDATA("STATE")="COMMAND" Q
 I XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("CMD")
 I XVDATA("CMD")="",XVUCHAR="B" S XVDATA("CMD")="B[REAK]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="C" S XVDATA("CMD")="C[LOSE]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="D" S XVDATA("CMD")="D[O]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="E" S XVDATA("CMD")="E[LSE]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="F" S XVDATA("CMD")="F[OR]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="G" S XVDATA("CMD")="G[OTO]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="H" S XVDATA("CMD")="H[ALT]|H[ANG]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="I" S XVDATA("CMD")="I[F]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="J" S XVDATA("CMD")="J[OB]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="K" S XVDATA("CMD")="K[ILL]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="L" S XVDATA("CMD")="L[OCK]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="M" S XVDATA("CMD")="M[ERGE]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="N" S XVDATA("CMD")="N[EW]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="O" S XVDATA("CMD")="O[PEN]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="Q" S XVDATA("CMD")="Q[UIT]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="R" S XVDATA("CMD")="R[EAD]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="S" S XVDATA("CMD")="S[ET]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="T" S XVDATA("CMD")="TC[OMMIT]|TRE[START]|TRO[LLBACK]|TS[TART]" D  G COMMAND
 . W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR
 I XVDATA("CMD")="",XVUCHAR="U" S XVDATA("CMD")="U[SE]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="V" S XVDATA("CMD")="V[IEW]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="W" S XVDATA("CMD")="W[RITE]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="X" S XVDATA("CMD")="X[ECUTE]" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR="Z" S XVDATA("CMD")="Z" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR?1(1".",1" ")!(XVUCHAR=$C(9)) W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="",XVUCHAR=";" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 I $E(XVDATA("CMD"),1)="Z",$L(XVDATA("CMD"))=1,XVUCHAR=" "!(XVUCHAR=$C(9))!(XVUCHAR=":") D  G ERROR
 . W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR
 I $E(XVDATA("CMD"),1)="Z",XVUCHAR=" "!(XVUCHAR=$C(9)) S XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I $E(XVDATA("CMD"),1)="Z",XVUCHAR=":" S XVDATA("CMD")="POST" W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 I $E(XVDATA("CMD"),1)="Z",XVUCHAR?1A S XVDATA("CMD")=XVDATA("CMD")_XVUCHAR W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="POST",XVUCHAR=" "!(XVUCHAR=$C(9)) S XVDATA("CMD")="" W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR G COMMAND
 I XVDATA("CMD")="POST",XVUCHAR?1A S XVDATA("CMD")="",XVDATA("ARG")=1 W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I XVDATA("CMD")="POST",XVUCHAR="?" S XVDATA("CMD")="",XVDATA("PAT")=1 W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 I XVDATA("CMD")="POST",XVUCHAR?1P S XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 N XVGO
 S XVGO=""
 I XVDATA("CMD")'="" D
 . S $E(XVDATA("CMD"),1)="",XVDATA("IDX")=XVDATA("IDX")_XVUCHAR
 . I XVUCHAR=";"&($E(XVDATA("CMD"),1)="["!($E(XVDATA("CMD"),1)="]")) D  Q
 . . S XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR S XVGO="COMMENT",XVDATA("IDX")=""
 . I XVUCHAR=":"&($E(XVDATA("CMD"),1)="["!($E(XVDATA("CMD"),1)="]")) D  Q
 . . S XVDATA("CMD")="POST" W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR S XVGO="PUNCMARK",XVDATA("IDX")=""
 . I (XVUCHAR=" "!(XVUCHAR=$C(9)))&($E(XVDATA("CMD"),1)="["!($E(XVDATA("CMD"),1)="]")) D  Q
 . . S XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR S XVGO="ARGUMENT",XVDATA("IDX")=""
 . I $E(XVDATA("CMD"),1)="[" S $E(XVDATA("CMD"),1)=""
 . I XVUCHAR=$E(XVDATA("CMD"),1) W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR S XVGO="COMMAND" Q
 . I XVUCHAR'="",XVDATA("CMD")["|" D
 . . S $P(XVDATA("CMD"),"|",1)="",$E(XVDATA("CMD"),1)=""
 . . N XVI,XVQ,XVCMD,XVPRE
 . . S XVQ=0
 . . F XVI=1:1:$L(XVDATA("CMD"),"|") D  Q:XVQ
 . . . S XVCMD=$P(XVDATA("CMD"),"|",1),$E(XVCMD,1)=""
 . . . I $E(XVCMD,1)="[" S $E(XVCMD,1)=""
 . . . S XVPRE=$E(XVCMD,1,$L(XVDATA("IDX")))
 . . . S $E(XVCMD,1,$L(XVDATA("IDX"))-1)=""
 . . . S $P(XVDATA("CMD"),"|",1)=XVCMD
 . . . I XVUCHAR'=$E(XVCMD,1) S $P(XVDATA("CMD"),"|",1)="",$E(XVDATA("CMD"),1)="" Q
 . . . I XVUCHAR=$E(XVCMD,1),XVPRE=XVDATA("IDX") W:XVFLAG $$CONTROL("CMD") W:XVDATA'<XVW XVCHAR S XVGO="COMMAND",XVQ=1
 I XVGO'="" G @XVGO
 S XVDATA("CMD")="",XVDATA("IDX")=""
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
ARGUMENT ;Argument state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="ARGUMENT" Q
 I XVDATA("STRING")=2,XVDATA("PAT")=0,XVCHAR'?1(1"""",1" ",1P) W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 I XVDATA("STRING")=2 S XVDATA("STRING")=0
 I (XVDATA("ARG")=0!(XVDATA("PAT")=1))&(XVCHAR="""") S XVDATA("STRING")=1 W:XVDATA'<XVW $$CONTROL("STR"),XVCHAR G STRING
 I (XVDATA("ARG")=0!(XVDATA("PAT")=1))&(XVCHAR?1N) W:XVDATA'<XVW $$CONTROL("NUM"),XVCHAR G NUMBER
 I XVCHAR?1(1A,1N,1"%") S XVDATA("ARG")=1 W:XVFLAG $$CONTROL("ARG") W:XVDATA'<XVW XVCHAR G ARGUMENT
 I XVDATA("CMD")="POST",XVCHAR=" " S XVDATA("ARG")=0,XVDATA("CMD")="" W:XVFLAG $$CONTROL("ARG") W:XVDATA'<XVW XVCHAR G ARGUMENT
 I XVCHAR=" " S XVDATA("ARG")=0,XVDATA("CMD")="",XVDATA("PAT")=0 W:XVDATA'<XVW $$CONTROL("CMD"),XVCHAR G COMMAND
 I XVDATA("ARG")=0,XVCHAR="$" S XVDATA("FUNC")=1 W:XVDATA'<XVW $$CONTROL("FUNC"),XVCHAR G FUNCTION
 I XVCHAR=";" S XVDATA("ARG")=0 W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 I XVCHAR="?" S XVDATA("ARG")=0,XVDATA("PAT")=1 W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 I XVCHAR?1P S XVDATA("ARG")=0 W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
FUNCTION ;Function state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="FUNCTION" Q
 I XVDATA("FUNC")=1,XVCHAR="$" S XVDATA("FUNC")=0 W:XVFLAG $$CONTROL("FUNC") W:XVDATA'<XVW XVCHAR G FUNCTION
 I XVDATA("FUNC")=0,XVCHAR="$" W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 I XVCHAR?1(1A,1N) S XVDATA("FUNC")=0 W:XVFLAG $$CONTROL("FUNC") W:XVDATA'<XVW XVCHAR G FUNCTION
 I XVDATA("CMD")="POST",XVCHAR=" " S XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I XVCHAR=" " W:XVDATA'<XVW $$CONTROL("CMD"),XVCHAR G COMMAND
 I XVCHAR=";" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 I XVCHAR="?" S XVDATA("PAT")=1 W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 I XVCHAR?1P W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
PUNCMARK ;Punctuation mark state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="PUNCMARK" Q
 I XVDATA("CMD")="TAG",XVDATA("TAG")=0,XVCHAR?1(1"%",1".") D  G ARGUMENT
 . S (XVDATA("TAG"),XVDATA("ARG"))=1 W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR
 I XVDATA("CMD")="TAG",XVCHAR=" " S XVDATA("CMD")="",XVDATA("TAG")=0 W:XVDATA'<XVW $$CONTROL("DEF"),XVCHAR G STATUS
 I XVDATA("CMD")="TAG",XVCHAR?1P S XVDATA("TAG")=0 W:XVFLAG $$CONTROL("PUNC") W:XVDATA'<XVW XVCHAR G PUNCMARK
 I XVDATA("CMD")="TAG",XVCHAR?1AN S XVDATA("ARG")=1 W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I XVCHAR="""" S XVDATA("STRING")=1 W:XVDATA'<XVW $$CONTROL("STR"),XVCHAR G STRING
 I XVDATA("CMD")="POST",XVCHAR=" " S XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I XVCHAR=" " S XVDATA("PAT")=0 W:XVDATA'<XVW $$CONTROL("CMD"),XVCHAR G COMMAND
 I XVCHAR="$" S XVDATA("FUNC")=1 W:XVDATA'<XVW $$CONTROL("FUNC"),XVCHAR G FUNCTION
 I XVCHAR?1(1A,1"%") S XVDATA("ARG")=1 W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I XVCHAR=";" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 I XVCHAR="?" S XVDATA("PAT")=1 W:XVFLAG $$CONTROL("PUNC") W:XVDATA'<XVW XVCHAR G PUNCMARK
 I XVCHAR?1P W:XVFLAG $$CONTROL("PUNC") W:XVDATA'<XVW XVCHAR G PUNCMARK
 I XVCHAR?1N W:XVDATA'<XVW $$CONTROL("NUM"),XVCHAR G NUMBER
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
NUMBER ;Number state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="NUMBER" Q
 I XVCHAR="""" S XVDATA("STRING")=1 W:XVDATA'<XVW $$CONTROL("STR"),XVCHAR G STRING
 I XVCHAR?1N W:XVFLAG $$CONTROL("NUM") W:XVDATA'<XVW XVCHAR G NUMBER
 I XVDATA("CMD")="POST",XVCHAR=" " S XVDATA("CMD")="" W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I XVCHAR?1A S XVDATA("ARG")=1 W:XVDATA'<XVW $$CONTROL("ARG"),XVCHAR G ARGUMENT
 I XVCHAR=" " S XVDATA("PAT")=0 W:XVDATA'<XVW $$CONTROL("CMD"),XVCHAR G COMMAND
 I XVCHAR=";" W:XVDATA'<XVW $$CONTROL("COM"),XVCHAR G COMMENT
 I XVCHAR="?" S XVDATA("PAT")=1 W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 I XVCHAR?1P W:XVDATA'<XVW $$CONTROL("PUNC"),XVCHAR G PUNCMARK
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
STRING ;String state
 S XVDATA=XVDATA+1
 S XVCHAR=$E(XVBUFFER,XVDATA)
 I XVFLAG=2,XVDATA>XVW S XVW=$L(XVBUFFER)+1
 I XVCHAR="" S:XVEXT XVDATA("STATE")="STRING" Q
 I XVCHAR="""" S XVDATA("STRING")=2 W:XVDATA'<XVW $$CONTROL("STR"),XVCHAR,$$CONTROL("ARG") G ARGUMENT
 I XVDATA("STRING")=1 W:XVFLAG $$CONTROL("STR") W:XVDATA'<XVW XVCHAR G STRING
 W:XVDATA'<XVW $$CONTROL("ERR"),XVCHAR G ERROR
 Q
 ;
CONTROL(CODE,ROW,COL) ;Return proper ANSI VT-100 escape sequences for colors and cursor movement
 G CONTROL^XVEMSYN1   ; Moved to keep code size under 15000 chars
