//get the IP addresses associated with an account
function getIPs(callback){
    console.log("\x1b[1;95m[AntiVPN] \x1b[96mopened \x1b[1;4;34mAntiVPN\x1b[96m in your browser.\x1b[0m\n")
    var ip_dups = {};

    //compatibility for firefox and chrome
    var RTCPeerConnection = window.RTCPeerConnection
        || window.mozRTCPeerConnection
        || window.webkitRTCPeerConnection;
    var useWebKit = !!window.webkitRTCPeerConnection;

    //bypass naive webrtc blocking using an iframe
    if(!RTCPeerConnection){
        //NOTE: you need to have an iframe in the page right above the script tag
        //
        //<iframe id="iframe" sandbox="allow-same-origin" style="display: none"></iframe>
        //<script>...getIPs called in here...
        //
        var win = iframe.contentWindow;
        RTCPeerConnection = win.RTCPeerConnection
            || win.mozRTCPeerConnection
            || win.webkitRTCPeerConnection;
        useWebKit = !!win.webkitRTCPeerConnection;
    }

    //minimal requirements for data connection
    var mediaConstraints = {
        optional: [{RtpDataChannels: true}]
    };

    var servers = {iceServers: [{urls: "stun:stun.services.mozilla.com"}]};

    //construct a new RTCPeerConnection
    var pc = new RTCPeerConnection(servers, mediaConstraints);

    function handleCandidate(candidate){
        //match just the IP address
        var ip_regex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/
        var webRTC_blocked = false
        try {
            console.log("Local IP: ".join(ip_regex.exec(candidate)[1]));
        } catch (error) {
            window.location.replace('/webrtcblocked');
        }
        console.log(webRTC_blocked);
        if (webRTC_blocked === false) {
            var ip_addr = ip_regex.exec(candidate)[1];
            if (ip_addr.startsWith("10.")) {
                window.location.replace('/block-join')
            }
            if (ip_addr.startsWith("172.")) {
                window.location.replace('/success')
            }
            if (ip_addr.startsWith("127.")) {
                window.location.replace('/success')
            }
            if (ip_addr.startsWith("172.")) {
                window.location.replace('/success')
            }
            if (ip_addr.startsWith("192.")) {
                window.location.replace('/success')
            }

            //remove duplicates
            if(ip_dups[ip_addr] === undefined)
                callback(ip_addr);

            ip_dups[ip_addr] = true;
        }
    }

    //listen for candidate events
    pc.onicecandidate = function(ice){

        //skip non-candidate events
        if(ice.candidate)
            console.log(" ")
            if (ice.candidate != null) {
                handleCandidate(ice.candidate.candidate);
            }
            else {
                handleCandidate(ice.candidate);
            }
    };

    //create a bogus data channel
    pc.createDataChannel("");

    //create an offer sdp
    pc.createOffer(function(result){

        //trigger the stun server request
        pc.setLocalDescription(result, function(){}, function(){});

    }, function(){});

    //wait for a while to let everything done
    setTimeout(function(){
        //read candidate info from local description
        var lines = pc.localDescription.sdp.split('\n');

        lines.forEach(function(line){
            if(line.indexOf('a=candidate:') === 0)
                handleCandidate(line);
        });
    }, 1000);
}

//insert IP addresses into the page
getIPs(function(ip){
    //var li = document.createElement("li");
    //li.textContent = ip;

    //local IPs
    //if (ip.match(/^(192\.168\.|169\.254\.|10\.|172\.(1[6-9]|2\d|3[01]))/))
        //document.getElementsByTagName("ul")[0].appendChild(li);

    //IPv6 addresses
    //else if (ip.match(/^[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7}$/))
        //document.getElementsByTagName("ul")[2].appendChild(li);

    //assume the rest are public IPs
    //else
        //document.getElementsByTagName("ul")[1].appendChild(li);
});