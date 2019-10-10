MODULE Module1
    VAR socketdev socket;
    VAR string receive_string;
    VAR num i:=0;
    VAR num latest_position:=0;
    VAR bool ok;

	PERS tooldata t_extruder := [TRUE, [[-185.368,-727.855,1308.16],[1, 0.0001, -0.0001, 0]], [150,[-92.684, -363.928, 654.08],[1,0,0,0],0,0,0]];

	CONST speeddata vel20 := [20,20,20,20];
	CONST speeddata vel100 := [100,100,100,100];
	CONST speeddata vel75 := [75,75,75,75];
	CONST speeddata vel25 := [25,25,25,25];

    PROC main()
	   SocketClose socket;
     SocketCreate socket;
     SocketConnect socket, "192.168.1.69", 12346;

		 ConfJ \Off;
		 ConfL \Off;

		 !WaitTime 5;

		ActUnit M7DM1;
		IndReset M7DM1, 1\RefNum:=0\Short;
		WaitTime 1;

        !Start position for robot
		MoveL [[1963.9, 358.8,-1050 ], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;

		!Start table
        IndCMove M7DM1,1,1000;
        WaitTime 4;
        server_send("{ ""command"": ""goto"",  ""speed"": 25,  ""points"": [89,99,109,119,129]}");


        MoveL [[1654.7, 407.1, -1050], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;

       Wait4Feedback(0);
		MoveL [[1963.9, 358.8, -1050], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;

        Wait4Feedback(1);
		MoveL [[1654.7, 407.1, -1050], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;


        Wait4Feedback(2);
		MoveL [[1963.9, 358.8, -1050], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;


        Wait4Feedback(3);
		MoveL [[1654.7, 407.1, -1050], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;


   Wait4Feedback(4);
     !test for ""points"": [129,119,109,99,89] to make programming for James easier
     server_send("{ ""command"": ""goto"",  ""speed"": 25,  ""points"": [119,109,99,89]}");

  MoveL [[1963.9, 358.8, -1044], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;

      Wait4Feedback(0);
  MoveL [[1654.7, 407.1, -1044], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;


     Wait4Feedback(1);
  MoveL [[1963.9, 358.8, -1044], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;


    Wait4Feedback(2);
MoveL [[1654.7, 407.1, -1044], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;

    Wait4Feedback(3);
MoveL [[1963.9, 358.8, -1044], [0.0, 0.95358, -0.30114, 0.0], [0,0,0,0], [0,9E9,9E9,9E9,9E9,9E9]], vel100, z10, t_extruder\WObj:=WObj0;


        IndCMove M7DM1,1,0;
        WaitTime 1.5;
        IndReset M7DM1,1\RefNum:=0\Short;
        WaitTime 1.5;


        SocketClose socket;


    ENDPROC


    !Procedure to send message to server and wait for response
    PROC server_send(string instruction)
        !Create and connect socket in error handler
        SocketSend socket\Str:=instruction;
        SocketReceive socket\Str:=receive_string;

    ERROR
        IF ERRNO=ERR_SOCK_TIMEOUT THEN
            !RETRY;
        ELSEIF ERRNO=ERR_SOCK_CLOSED THEN
            !client_recover;
            !RETRY;
        ELSE
            !No error recovery handling
        ENDIF
    ENDPROC

    PROC Wait4Feedback(intnum a)

        !Create and connect socket in error handler
        SocketSend socket \Str:= "{""command"": ""getCurrentIndex""}";
        SocketReceive socket \Str:=receive_string;
        latest_position:=-1;
        ok := StrToVal(receive_string,latest_position);
        WHILE (latest_position < a) DO

            !TPWrite "in while loop";
            WaitTime 0.2;
            SocketSend socket \Str:= "{""command"": ""getCurrentIndex""}";
			!ValToStr(a);
            SocketReceive socket \Str:=receive_string;
            ok := StrToVal(receive_string, latest_position);

        ENDWHILE
		!TPWrite receive_string;

    ENDPROC



    !procedure to handle error if socket connection has error
    PROC client_recover()
        SocketClose socket;
        SocketCreate socket;
        SocketConnect socket, "192.168.1.69", 12346;
        !server ip address and port number

    ERROR
        IF ERRNO=ERR_SOCK_TIMEOUT THEN
            !RETRY;
        ELSEIF ERRNO=ERR_SOCK_CLOSED THEN
            !RETRY;
        ELSE
            !No error
        ENDIF

    ENDPROC



ENDMODULE
