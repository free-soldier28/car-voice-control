class VoskConfig:
    def __init__(self, lang, commands, model_path, use_activation, activation_words, activation_timeout, sample_rate=16000):
        self.lang = lang
        self.commands = commands
        self.model_path = model_path
        self.use_activation = use_activation
        self.activation_words = activation_words
        self.activation_timeout = activation_timeout
        self.sample_rate = sample_rate
