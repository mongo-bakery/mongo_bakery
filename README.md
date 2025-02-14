# mongo_bakery

# Motivação
- Ter as facilidades do model_bakery (do mundo django) no Flask com mongo engine
- Queremos ter mais contexto no próprio teste (ao inves de um fixtures lá no conftest que não sabemos quais campos estão preenchidos)
- Não queremos ter que criar uma Factory para cada Document da aplicação

# Alteranativas
- https://factoryboy.readthedocs.io/en/stable/
- https://github.com/klen/mixer

# Rascunho da solução
- https://gist.github.com/huogerac/57d2ecc15b1ba8fc16af41a697065f24
