class FFmpegCommandBuilder:
    def __init__(self, ffmpegPath="ffmpeg"):
        self.ffmpegPath = ffmpegPath
        self.command = [self.ffmpegPath]
        self._inputFiles = []
        self._filterComplex = []
        self._videoFilters = []
        self._audioFilters = []
        self._videoCodec = None
        self._audioCodec = None
        self._videoBitrate = None
        self._audioBitrate = None
        self._videoFramerate = None
        self._videoResolution = None
        self._videoAspectRatio = None
        self._videoPreset = None
        self._outputFile = None
        self._crf = None

    def addInput(self, inputFile):
        self._inputFiles.append(inputFile)
        return self

    def complexFilter(self, filter):
        self._filterComplex.append(filter)
        return self

    def complexFilterChain(self, filterChain):
        self._filterComplex.append(filterChain)
        return self

    def complexFilterForInput(self, filter, inputIndex):
        self._filterComplex.append(f"[{inputIndex}] {filter}")
        return self

    def videoFilter(self, filter):
        self._videoFilters.append(filter)
        return self

    def audioFilter(self, filter):
        self._audioFilters.append(filter)
        return self

    def videoCodec(self, codec):
        self._videoCodec = codec
        return self

    def audioCodec(self, codec):
        self._audioCodec = codec
        return self

    def videoBitrate(self, bitrate):
        self._videoBitrate = bitrate
        return self

    def audioBitrate(self, bitrate):
        self._audioBitrate = bitrate
        return self

    def videoFramerate(self, framerate):
        self._videoFramerate = framerate
        return self

    def videoResolution(self, width=None, height=None, resString=None):
        if resString is not None:
            self._videoResolution = resString
            return self
        else:
            if width is None or height is None:
                raise Exception("Width and height must be specified")

        self._videoResolution = f"{width}x{height}"
        return self

    def videoAspectRatio(self, aspectRatio):
        self._videoAspectRatio = aspectRatio
        return self

    def videoPreset(self, preset):
        self._videoPreset = preset
        return self

    def OverwriteOutput(self):
        self.command.append("-y")
        return self

    def overlayFilter(self, baseIndex, OverlayIndex, x, y, outlabel=None):
        filter = f"[{baseIndex}][{OverlayIndex}]overlay={x}:{y}"
        if outlabel is not None:
            filter += f"[{outlabel}]"
        self._filterComplex.append(filter)
        return self

    def resizeFilter(self, inputIndex, width, height, outlabel=None):
        filter = f"[{inputIndex}]scale={width}:{height}"
        if outlabel is not None:
            filter += f"[{outlabel}]"
        self._filterComplex.append(filter)
        return self

    def scale2refFilter(self, inputIndex, refIndex, filter, outlabel=None, refoutlabel=None):
        filter = f"[{inputIndex}][{refIndex}]scale2ref={filter}"
        if outlabel is not None:
            filter += f"[{outlabel}]"
        if refoutlabel is not None:
            filter += f"[{refoutlabel}]"

        self._filterComplex.append(filter)
        return self

    def output(self, outputFile):
        self._outputFile = outputFile
        return self

    def crf(self, crf):
        self._crf = crf
        return self

    def build(self):
        if len(self._inputFiles) == 0:
            raise FFmpegCommandBuilderException("No input files specified")

        if self._outputFile is None:
            raise FFmpegCommandBuilderException("No output file specified")

        for inputFile in self._inputFiles:
            self.command.append("-i")
            self.command.append(inputFile)
        if len(self._filterComplex) > 0:
            self.command.append("-filter_complex")
            self.command.append(",".join(self._filterComplex))

        if len(self._videoFilters) > 0:
            self.command.append("-vf")
            self.command.append(",".join(self._videoFilters))

        if len(self._audioFilters) > 0:
            self.command.append("-af")
            self.command.append(",".join(self._audioFilters))

        if self._videoCodec is not None:
            self.command.append("-vcodec")
            self.command.append(self._videoCodec)

        if self._audioCodec is not None:
            self.command.append("-acodec")
            self.command.append(self._audioCodec)

        if self._videoBitrate is not None:
            self.command.append("-b:v")
            self.command.append(str(self._videoBitrate))

        if self._audioBitrate is not None:
            self.command.append("-b:a")
            self.command.append(str(self._audioBitrate))

        if self._videoFramerate is not None:
            self.command.append("-r")
            self.command.append(str(self._videoFramerate))

        if self._videoResolution is not None:
            self.command.append("-s")
            self.command.append(str(self._videoResolution))

        if self._videoAspectRatio is not None:
            self.command.append("-aspect")
            self.command.append(str(self._videoAspectRatio))

        if self._videoPreset is not None:
            self.command.append("-preset")
            self.command.append(str(self._videoPreset))

        if self._crf is not None:
            if self._videoCodec is None:
                raise FFmpegCommandBuilderException("CRF can only be used with a video codec")
            if self._videoCodec != "libx264" or self._videoCodec != "libx265":
                raise FFmpegCommandBuilderException("CRF can only be used with libx264 or libx265")

            self.command.append("-crf")
            self.command.append(str(self._crf))

        self.command.append(self._outputFile)

        return self.command


class FFmpegCommandBuilderException(Exception):
    pass
