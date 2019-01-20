MS AS WBXML Decoder Burp Extension
==============

A Burp Extension for decoding Microsoft Active-Sync WAP Binary XML (WBXML) Written in Python

Written by Chereddi, Phanikar EMAIL: phanikar DOT chereddi AT spirent.com

Added a wrapper arround the below project to extend Burp Suite
https://github.com/davidpshaw/PyWBXMLDecoder

Changes to original PyWBXMLDecoder
==============
Original decoder was written in Python 3 and Burp Extensions needed it to be Python 2.7. So, I had to make few changes to the original Decoder.

Description
==============

I was pentesting a email client mobile app that was using MS-AS-WBXML. I use Burp as my proxy tool and I could not find any Burp extensions that could decode WBXMl. Eventhough other proxy tools had extension for decoding WBXML, I did want to swith my super favourite tool. So here it is...

I found this guy @davidpshaw awesome project and wrote a wrapper arround so that I can continue using Burp for my pentest.

For now, this extension supports only decoding the WBXML.

Once you have loaded this extension you will see a "WBXML" tab whenever the "content-type" header in your HTTP request or HTTP response has the keyword "wbxml" in it. This tab will be added in the following tools of Burp Suite:

* Proxy
* Repeater

Burp Extender Install Instructions
==============

I used the jython-standalone-2.7.0.jar that is in the repo.
I recommed using the same jar, unless it messes up other extension you installed. I had some issues when I was trying to load other python extension written by my friends

1. Download the jython-standalone-2.7.0.jar form this repo and provide the path where downloaded it to in Burp:

    ```sh
    Extender >>> Options >>> Python Environment >>> Location of Jython standalone JAR file
    ```

2. Install the extension by going to:
    ```sh
    Extender >>> Extensions >>> Burp Extensions
    ```
	    Extension type: Python
	    Extension file (.py): ms_as_wbxml_decoder.py


Spirent SecurityLabs Rocks! kudos to them for letting me OpenSource this code!
[![N|Solid](https://www.spirent.com/-/media/logoblack2017-2/logo.svg?la=en&hash=78A1E2634AEF02CDCC6D0B298D7E0078E2E40357)](https://nodesource.com/products/nsolid)

