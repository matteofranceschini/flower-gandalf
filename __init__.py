from st3m.application import Application, ApplicationContext
import st3m.run
import leds
import uos
import bl00mbox


SONG_SAX_GUY_FLASH = "/flash/sys/samples/epicsaxguy-cut.wav"
SONG_SAX_GUY = "/sd/epicsaxguy-cut.wav"

class Gandalf(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.picidx: int = 0; 
        self.elapsed: int = 3000
        self.channel = bl00mbox.Channel("Gandalf")
        self.channel.volume = 5000
        self.samples = {}


    def draw(self, ctx: Context) -> None:
        # Paint the background black
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()

        path = self.nextImage(ctx)
        ctx.image(path, -120, -120, 241, 241)


    def nextImage(self, ctx: Context):
        path = f"/flash/sys/apps/teo-gandalf/frame_{str(self.picidx)}.png"
        self.picidx = self.picidx + 2
        if self.picidx > 10:
           self.picidx = 0
        return path

    def think(self, ins: InputState, delta_ms: int) -> None:
        if len(self.samples) == 0:
            sample = self.channel.new(bl00mbox.patches.sampler, SONG_SAX_GUY)
            sample.signals.output = self.channel.mixer
            self.samples["saxguy"] = sample
        self.elapsed += delta_ms
        if self.elapsed > 2500:
            self.samples["saxguy"].signals.trigger.start()
            self.elapsed = 0
        super().think(ins, delta_ms) # Let Application do its thing
        
        



if __name__ == '__main__':
    st3m.run.run_view(Gandalf(ApplicationContext()))
