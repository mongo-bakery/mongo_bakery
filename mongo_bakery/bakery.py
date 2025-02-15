class Baker:

    def make(self, model_class):
        return model_class()


baker = Baker()
