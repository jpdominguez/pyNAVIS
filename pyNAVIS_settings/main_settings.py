class MainSettings:

    mono_stereo = 0


    bin_size = 20000
    ts_tick = 0.2
    num_channels = 32
    address_size = 2

    on_off_both = 2

    reset_timestamp = True

    spikegram_dot_size = 0.1

    bar_line = 1




    def __init__(self, p_num_channels, p_mono_stereo, p_address_size, p_ts_tick, p_bin_size, p_on_off_both = 2, p_reset_timestamp = True, p_spikegram_dot_size = 0.1, p_bar_line = 1):
        self.num_channels = p_num_channels
        self.mono_stereo = p_mono_stereo
        self.address_size = p_address_size
        self.ts_tick = p_ts_tick
        self.bin_size = p_bin_size
        self.on_off_both = p_on_off_both
        self.reset_timestamp = p_reset_timestamp
        self.spikegram_dot_size = p_spikegram_dot_size
        self.bar_line = p_bar_line
