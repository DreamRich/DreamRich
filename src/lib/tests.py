def test_create_historic(self, model, factory):
    count = model.history.count()
    factory()
    self.assertTrue(model.history.count() > count)


def test_all_create_historic(self, models, factory):
    for model in models:
        test_create_historic(self, model, factory)
