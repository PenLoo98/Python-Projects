# 107~109

def generate_request():
    with MS.MicrophoneStream(RATE, CHUNK) as stream: 
    audio_generator = stream.generator()
    messageReq = gigagenieRPC_pb2.reqQueryVoice()
    messageReq.reqOptions.lang=0
    messageReq.reqOptions.userSession="1234"
    messageReq.reqOptions.deviceId="aklsjdnalksd" 
    yield messageReq
    for content in audio_generator:
        message = gigagenieRPC_pb2.reqQueryVoice() 
        message.audioContent = content
        yield message
        rms = audioop.rms(content,2)

def queryByVoice():
    print ("\n\n\n질의할 내용을 말씀해 보세요.\n\n듣고 있는 중......\n")
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials()) 
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    request = generate_request() 
    resultText = ''
    response = stub.queryByVoice(request) 
    if response.resultCd == 200:
        print("질의 내용: %s" % (response.uword))
        for a in response.action:
            response = a.mesg
            parsing_resp = response.replace('<![CDATA[', '') 
            parsing_resp = parsing_resp.replace(']]>', '') 
            resultText = parsing_resp
            print("\n질의에 대한 답변: " + parsing_resp +'\n\n\n')   

    else: 
        print("\n\nresultCd: %d\n" % (response.resultCd))
        print("정상적인 음성인식이 되지 않았습니다.")
    return resultText

def main():
    queryByVoice() 
    time.sleep(0.5)

if __name__ == '__main__': 
    main()

def generate_request():
    with MS.MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        messageReq = gigagenieRPC_pb2.reqQueryVoice()
        messageReq.reqOptions.lang=0
        messageReq.reqOptions.userSession="1234"
        messageReq.reqOptions.deviceId="aklsjdnalksd" 
        yield messageReq
        for content in audio_generator:
            message = gigagenieRPC_pb2.reqQueryVoice() 
            message.audioContent = content
            yield message
            rms = audioop.rms(content,2)

def queryByVoice():
    print ("\n\n\n질의할 내용을 말씀해 보세요.\n\n듣고 있는 중......\n")
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials()) 
    stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
    request = generate_request() 
    resultText = ''
    response = stub.queryByVoice(request) 
    if response.resultCd == 200:
        print("질의 내용: %s" % (response.uword)) 
        for a in response.action:
            response = a.mesg
            parsing_resp = response.replace('<![CDATA[', '') 
            parsing_resp = parsing_resp.replace(']]>', '') 
            resultText = parsing_resp
            print("\n질의에 대한 답변: " + parsing_resp +'\n\n\n')
            
    else:
        print("\n\nresultCd: %d\n" % (response.resultCd)) 
        print("정상적인 음성인식이 되지 않았습니다.")
    return resultText