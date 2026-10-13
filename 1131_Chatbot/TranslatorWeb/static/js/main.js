$(function(){
    $("#TranslatedVoice_Default").hide();
    $("#TranslatedVoice_Chat").hide();
    $("#TranslatedVoice_Cheerful").hide();
    $("#TranslatedVoice_CustomerService").hide();

    $("#submit").click(azureTranslate);
    $("#message").keypress(function (e) {
        if (e.which == 13) {
            azureTranslate();
        }
    });
    $("#TranslatedVoice_Default").click(function () {
        $("#myAudio_Default").attr("src", "");
        // add a random query string to the audio source to prevent caching
        $("#myAudio_Default").attr("src", "/static/outputaudio_default.wav?a=" + Math.random());
        $("#myAudio_Default")[0].load();
        $("#myAudio_Default")[0].play();
    });
    $("#TranslatedVoice_Chat").click(function () {
        $("#myAudio_Chat").attr("src", "");
        // add a random query string to the audio source to prevent caching
        $("#myAudio_Chat").attr("src", "/static/outputaudio_chat.wav?a=" + Math.random());
        $("#myAudio_Chat")[0].load();
        $("#myAudio_Chat")[0].play();
    });
    $("#TranslatedVoice_Cheerful").click(function () {
        $("#myAudio_Cheerful").attr("src", "");
        // add a random query string to the audio source to prevent caching
        $("#myAudio_Cheerful").attr("src", "/static/outputaudio_cheerful.wav?a=" + Math.random());
        $("#myAudio_Cheerful")[0].load();
        $("#myAudio_Cheerful")[0].play();
    });
    $("#TranslatedVoice_CustomerService").click(function () {
        $("#myAudio_CustomerService").attr("src", "");
        // add a random query string to the audio source to prevent caching
        $("#myAudio_CustomerService").attr("src", "/static/outputaudio_customerservice.wav?a=" + Math.random());
        $("#myAudio_CustomerService")[0].load();
        $("#myAudio_CustomerService")[0].play();
    });
});

function azureTranslate() {
    $("#InputText").empty();
    $("#TranslatedText").empty();
    $("#TranslatedVoice_Default").hide();
    $("#TranslatedVoice_Chat").hide();
    $("#TranslatedVoice_Cheerful").hide();
    $("#TranslatedVoice_CustomerService").hide();

    var message = $("#message").val();
    $("#InputText").text(message);
    var params = {
        message: message
    };
    $.post("/azure_translate", params, function (data) {
        $("#TranslatedText").text(data);
        $("#TranslatedVoice_Default").show();
        $("#TranslatedVoice_Chat").show();
        $("#TranslatedVoice_Cheerful").show();
        $("#TranslatedVoice_CustomerService").show();
    });
    $("#message").val("");
}