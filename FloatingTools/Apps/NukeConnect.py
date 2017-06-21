# ft imports
import FloatingTools
from App import App


class NukeConnect(App):

    ICON = 'https://s3.amazonaws.com/fxhome-static/images/product/ignite-pro-2017/foundry-nuke.png'

    def animationSwitch(self):
        return self.redirect(self.arguments()['sourcePage'], knobAnimation=self.arguments()['knob'])

    def sendNodes(self):
        try:
            # execute node copy to the clipboard inside nuke
            FloatingTools.wrapper().nuke.nodeCopy(FloatingTools.wrapper().nukescripts.cut_paste_file())

            # pull data for sending
            nodeData = FloatingTools.wrapper().PySide.QtGui.QApplication.clipboard().text()

            # send the data
            self.send({'nodeSend': nodeData}, self.arguments()['sendTo'])
        except:
            return FloatingTools.Dashboard.ErrorPage().render()

    def receive(self, data):
        if 'nodeSend' in data:
            FloatingTools.wrapper().PySide.QtGui.QApplication.clipboard().setText(data['nodeSend'])
            FloatingTools.wrapper().nuke.nodePaste(FloatingTools.wrapper().nukescripts.cut_paste_file())

    def buildUI(self):
        """
        App UI
        """
        # get network environment
        peers = FloatingTools.Dashboard.dashboardEnv()['ft_peers']

        # layout page
        mainRow = FloatingTools.Dashboard.Row()
        mainRow.addColumn(6)

        # get all of the selected nodes.
        selectedNodes = FloatingTools.wrapper().nuke.selectedNodes()
        selectionCount = len(selectedNodes)

        if selectionCount > 0:
            # build main send panel
            nodePanel = FloatingTools.Dashboard.Panel('Send')

            panelLayout = FloatingTools.Dashboard.Row()
            panelLayout.addColumn(6)
            panelLayout.addColumn(6)

            # panel node send section
            userLabel = FloatingTools.Dashboard.Element('label', 'Send to')
            peerSelect = FloatingTools.Dashboard.Select('send-node')
            for peer in peers:
                if peers[peer]['application'] == 'Nuke':
                    peerSelect.addOption(peers[peer]['host'], peers[peer]['user'])
            userLabel.addValue(peerSelect)

            nodePanel.addToHeader(userLabel)

            if selectionCount == 1:
                selectionLabel = FloatingTools.Dashboard.Element('label', str(len(selectedNodes)) + ' node selected.')
            else:
                selectionLabel = FloatingTools.Dashboard.Element('label', str(len(selectedNodes)) + ' nodes selected.')

            sendButton = FloatingTools.Dashboard.Form.submit('Send Nodes')
            self.connectToElement(sendButton, self.sendNodes, sendTo=peerSelect)

            # layout panel
            panelLayout.addToColumn(selectionLabel, 0)
            panelLayout.addToColumn(FloatingTools.Dashboard.Hr(), 0)
            nodeList = FloatingTools.Dashboard.List()
            panelLayout.addToColumn(nodeList, 0)

            for node in selectedNodes:
                item = nodeList.addItem(
                    FloatingTools.Dashboard.Center(
                        FloatingTools.Dashboard.Font(node.name(), color='green', size=5)
                    )
                )
                knobList = FloatingTools.Dashboard.List()
                item.addValue(knobList)
                for name, knob in node.knobs().iteritems():
                    try:
                        if knob.value() != knob.defaultValue():
                            knobList.addItem(name + ': ' + str(knob.value()))
                    except:
                        pass


            nodePanel.addToFooter(sendButton)

            # pull animation data from all the nodes selected
            curves = {}

            for node in FloatingTools.wrapper().nuke.selectedNodes():
                for knob in node.knobs().values():
                    try:
                        if knob.isAnimated():
                            for curve in knob.animations():
                                curves[node.name() + '.' + curve.knobAndFieldName()] = curve
                    except AttributeError:
                        continue

            knobLabel = FloatingTools.Dashboard.Element('label', 'Knob')
            knobSelect = FloatingTools.Dashboard.Select('knob-select')
            knobLabel.addValue(knobSelect)

            self.connectToElement(knobSelect, self.animationSwitch, flag='onchange', knob=knobSelect)

            sortedCurves = sorted(curves)
            try:
                target = sortedCurves[0]
                for curve in sortedCurves:
                    opt = knobSelect.addOption(curve, text=curve)

                    if 'knobAnimation' not in self.arguments():
                        continue

                    if curve == self.arguments()['knobAnimation']:
                        opt.addFlag('selected')
                        target = curve

                curveData = {}

                for animationData in curves[target].keys():
                    curveData[animationData.x] = animationData.y

                sendAnimation = FloatingTools.Dashboard.Form.submit('Send Animation')

                panelLayout.addToColumn(knobLabel, 1)
                panelLayout.addToColumn(FloatingTools.Dashboard.LineGraph('Value', curveData, 10, 300), 1)
                nodePanel.addToFooter(sendAnimation)
            except IndexError:
                panelLayout.addToColumn(FloatingTools.Dashboard.Header('No Animation Data Found', 3), 1)
                pass

            # add the panels layout
            nodePanel.addTobody(panelLayout)

            # add to row
            mainRow.addToColumn(nodePanel, 0)

        # build page
        self.page().add(mainRow)


if FloatingTools.wrapperName() == 'Nuke':
    NukeConnect()