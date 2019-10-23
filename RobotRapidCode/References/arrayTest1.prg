MODULE loopThru

  ! peristent JSON
  CONST num maxarraysize := 128;
  VAR string JSONParts{128};
  VAR num arraysize:=0;
  VAR num currentarraysize:=0;

  ! delcare socket variables
  VAR socketdev socket;
  VAR string receive_string;
  VAR num i:=0;
  VAR num latest_position:=0;
  VAR bool ok;

  ! Run main
  PROC main()
    ! create and connect the socket
    SocketClose socket;
    SocketCreate socket;
    SocketConnect socket, "192.168.1.59", 12346;

    initarray; ! call this before each arc is sent
    insertelement("{""command"":""goThroughPoints"",""speed"":100,""points"":[1.5,3,4.5,6,7.5,9,10.5,12");
    insertelement(",13.5,15,16.5,18,19.5,21,22.5,24,25.5,27,28.5,30]}");
    sendAll; ! send all the JSON parts to the server
    WaitTime 45;

    initarray; ! call this before each arc is sent
    insertelement("{ ""command"": ""goThroughPoints"",  ""speed"": 100,  ""points"": [89,99,109,119,129]}");
    sendAll; ! send all the JSON parts to the server
    WaitTime 45;

    initarray; ! call this before each arc is sent
    insertelement("{""command"":""goThroughPoints"",""speed"":100,""points"":[1.5,3,4.5,6,7.5,9,10.5,12");
    insertelement(",13.5,15,16.5,18,19.5,21,22.5,24,25.5,27,28.5,30.2,");
    insertelement("40,41,45,46,48,55]}");
    sendAll; ! send all the JSON parts to the server
    WaitTime 45;

  ENDPROC

  PROC initarray()
    currentarraysize:=0;
  ENDPROC

  PROC insertelement(string text)
    currentarraysize:=currentarraysize+1;
    JSONParts{currentarraysize}:=text;
  ENDPROC


  PROC server_send(string instruction)
      !Create and connect socket in error handler
      SocketSend socket\Str:=instruction;
      SocketReceive socket\Str:=receive_string;

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

  !procedure to handle error if socket connection has error
  PROC client_recover()
      SocketClose socket;
      SocketCreate socket;
      SocketConnect socket, "192.168.1.59", 12346;
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

  PROC sendAll()
    FOR i FROM 1 TO currentarraysize DO
      server_send JSONParts{i};
    ENDFOR
  ENDPROC

  PROC e_stop()
      TPWrite "STOPPING TABLE";
      SocketClose socket;
      SocketCreate socket;
      SocketConnect socket, "192.168.1.59", 12346;
      server_send("{ ""command"": ""stop""}");
  ENDPROC

  PROC resend_arc()

  ENDPROC


ENDMODULE
