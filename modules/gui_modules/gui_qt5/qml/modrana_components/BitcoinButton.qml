//BitcoinButton.qml

import QtQuick 2.0
import UC 1.0

Rectangle {
    id : bitcoinButton
    color : bitcoinMA.pressed ? "silver" : "black"
    radius : 25
    border.width : 2
    border.color : "white"
    width : 210 * rWin.c.style.m
    height : rWin.c.style.button.generic.height * 0.85
    property string url : ""

    Label {
        anchors.horizontalCenter : parent.horizontalCenter
        anchors.verticalCenter : parent.verticalCenter
        font.family: "Arial"
        font.pixelSize : 24 * rWin.c.style.m
        text : "<b>Bitcoin</b>"
        color : bitcoinMA.pressed ? "black" : "white"
        width : parent.width
        horizontalAlignment : Text.AlignHCenter
        verticalAlignment : Text.AlignVCenter
    }
    MouseArea {
        id : bitcoinMA
        anchors.fill : parent
        onClicked : {
            console.log('Bitcoin button clicked')
            bitcoinDialog.open()
        }
    }

    /*
    Dialog {
        id : bitcoinDialog
        width : parent.width - 30 * rWin.c.style.m
        //property Style platformStyle: SelectionDialogStyle {}
        property string titleText: "Bitcoin address"
        title: Item {
            id: header
            height: bitcoinDialog.platformStyle.titleBarHeight
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            Item {
                id: labelField
                anchors.fill:  parent
                Item {
                    id: labelWrapper
                    anchors.left: parent.left
                    anchors.right: closeButton.left
                    anchors.bottom:  parent.bottom
                    anchors.bottomMargin: bitcoinDialog.platformStyle.titleBarLineMargin
                    height: titleLabel.height
                    Label {
                        id: titleLabel
                        x: bitcoinDialog.platformStyle.titleBarIndent
                        width: parent.width - closeButton.width
                        font: bitcoinDialog.platformStyle.titleBarFont
                        color: bitcoinDialog.platformStyle.commonLabelColor
                        elide: bitcoinDialog.platformStyle.titleElideMode
                        text: bitcoinDialog.titleText
                    }

                }
                Image {
                    id: closeButton
                    anchors.verticalCenter : labelWrapper.verticalCenter
                    anchors.right: labelField.right
                    opacity: closeButtonArea.pressed ? 0.5 : 1.0
                    source: "image://theme/icon-m-common-dialog-close"
                    MouseArea {
                        id: closeButtonArea
                        anchors.fill: parent
                        onClicked:  {bitcoinDialog.reject();}
                    }
                }
            }

            Rectangle {
                id: headerLine

                anchors.left: parent.left
                anchors.right: parent.right

                anchors.bottom:  header.bottom

                height: 1

                color: "#4D4D4D"
            }
        }

        content:Item {
            id: dialogContent
            width : parent.width
            height : bitcoinQrCode.height + urlField.height + rWin.c.style.main.spacingBig * 2
            Image {
                id : bitcoinQrCode
                anchors.top : dialogContent.top
                anchors.topMargin : rWin.c.style.main.spacing
                anchors.horizontalCenter : parent.horizontalCenter
                source : "image://python/icon/" + rWin.theme.id + "/qrcode_bitcoin.png"
            }
            TextInput {
                id : urlField
                anchors.top : bitcoinQrCode.bottom
                anchors.topMargin : rWin.c.style.main.spacing
                anchors.left : parent.left
                anchors.right : parent.right
                //anchors.horizontalCenter : parent.horizontalCenter
                font.pointSize : 20 * rWin.c.style.m
                height : 48 * rWin.c.style.m
                text : bitcoinButton.url
                //color : "white"
                onTextChanged : {
                    selectAll()
                }
            }
            Button {
                anchors.top : urlField.bottom
                anchors.topMargin : 12 * rWin.c.style.m
                anchors.horizontalCenter : parent.horizontalCenter
                text: "Copy address"
                //iconSource : "image://theme/icon-m-toolbar-cut-paste"
                onClicked: {
                    urlField.selectAll()
                    urlField.copy()
                    rWin.notify("Bitcoin address copied to clipboard", 3000)
                }
            }
        }

    }*/

}


