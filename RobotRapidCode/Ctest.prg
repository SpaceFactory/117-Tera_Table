MODULE Module1
    !***********************************************************
    !
    ! Module:  Module1
    !
    ! Description:
    !   <Insert description here>
    !
    ! Author: AIShared
    !
    ! Version: 1.0
    !
    !***********************************************************
    !***********************************************************
    !
    ! Procedure main
    !
    ! This is the entry point of your program
    !
    !***********************************************************
    !Declaration varaibles
    VAR socketdev socket;
    VAR string receive_string;
    VAR num i:=0;
    !"{ ""command "": "" goto "",          "" speed "": 100,    ""points"": [89,90,91,92]}";

    PERS tooldata t_extruder:=[TRUE,[[-185.368,-727.855,1308.16],[1,0.0001,-0.0001,0]],[150,[-92.684,-363.928,654.08],[1,0,0,0],0,0,0]];

    CONST speeddata vel20:=[20,20,20,20];
    CONST speeddata vel100:=[100,100,100,100];
    CONST speeddata vel75:=[75,75,75,75];
    CONST speeddata vel25:=[25,25,25,25];

    CONST robtarget p1:=[[10,0,1000],[0,0.1305,0.9914,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];
    CONST robtarget p2:=[[10,100,1000],[0,0.1305,0.9914,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];

    PROC main()
        ConfJ\Off;
        ConfL\Off;

        WaitTime 1;

        !! Exterior of beam
        MoveL [[1662.822,0,-1204],[0,-0.6088,0.7934,0],[0,0,0,0],[0,9E9,9E9,9E9,9E9,9E9]],vel100,z10,t_extruder\WObj:=WObj0;
        !IndCMove M7DM1,1 ,1000;

        !! Turn on extruder
        !IndCMove M7DM1,1 ,1000;
        !WaitTime 1.5;

        !set current position as home
        server_send("{ ""command "": ""setHome""}");

        !send the vector of angles
        server_send("{ ""command "": "" goto "",      "" speed "": 100,    ""points"": [0,5,10,15,20]}");

        !Query server to confirm whether the position is reached

         Wait4Feedback (0);
         Wait4Feedback (1);
         Wait4Feedback (2);
         Wait4Feedback (3);
         Wait4Feedback (4);

        !! Move the turn table across arc "A" -45 degree
        !! Code goes here

        !! Interior of beam
        MoveL [[1882.822,0,-1204],[0,-0.6088,0.7934,0],[0,0,0,0],[0,9E9,9E9,9E9,9E9,9E9]],vel100,z10,t_extruder\WObj:=WObj0;

        server_send("{ ""command "": "" goto "",  "" speed "": 100, ""points"": [20,15,10,5,0]}");

         Wait4Feedback (0);
         Wait4Feedback (1);
         Wait4Feedback (2);
         Wait4Feedback (3);
         Wait4Feedback (4);

        !! Move the turn table across arc "C" 45 degree
        !! Code goes here

        !! Extruder Off
        !IndCMove M7DM1,1,0;
        WaitTime 1.5;
        !IndReset M7DM1,1\RefNum:=0\Short;
        WaitTime 1.5;

        !! Move to home
        MoveAbsJ [[0,0,0,0,90,-75],[0,9E9,9E9,9E9,9E9,9E9]],vel100,z10,t_extruder\WObj:=WObj0;
        SocketClose socket;


    ENDPROC



    !Procedure to send message to server and wait for response
    PROC server_send(string instruction)
        !Create and connect socket in error handler
        SocketSend socket \Str:= instruction;
        SocketReceive socket \Str:=receive_string;


    ERROR
        IF ERRNO=ERR_SOCK_TIMEOUT THEN
            RETRY;
        ELSEIF ERRNO=ERR_SOCK_CLOSED THEN
            client_recover;
            RETRY;
        ELSE
            !No error recovery handling
        ENDIF
    ENDPROC

    PROC Wait4Feedback(intnum a)
        !Create and connect socket in error handler
        SocketSend socket \Str:= ValToStr(a) ;
        SocketReceive socket \Str:=receive_string;
        VAR num latest_position:=0;
        StrToVal(receive_string,latest_position);
        WHILE (latest_position < a) DO
            WaitTime 0.05;
            SocketSend socket \Str:= ValToStr(a) ;
            SocketReceive socket \Str:=receive_string;
            StrToVal(receive_string,latest_position);
        ENDWHILE
    ENDPROC



    !procedure to handle error if socket connection has error
    PROC client_recover()
        SocketClose socket;
        SocketCreate socket;
        SocketConnect socket,"192.168.1.69",12346;
        !server ip address and port number

    ERROR
        IF ERRNO=ERR_SOCK_TIMEOUT THEN
            RETRY;
        ELSEIF ERRNO=ERR_SOCK_CLOSED THEN
            RETRY;
        ELSE
            !No error
        ENDIF

    ENDPROC



ENDMODULE
