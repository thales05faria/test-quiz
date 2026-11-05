import pytest
from model import Question, Choice


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

#NOVOS TESTES

# 1. Testar se os IDs das escolhas são gerados e incrementados corretamente
def test_add_multiple_choices_generates_correct_ids():
    question = Question(title='Q1')
    c1 = question.add_choice('A')
    c2 = question.add_choice('B')
    assert c1.id == 1
    assert c2.id == 2
    assert len(question.choices) == 2

# 2. Testar a remoção de uma escolha pelo ID
def test_remove_choice_by_id():
    question = Question(title='Q1')
    question.add_choice('A')
    question.remove_choice_by_id(1)
    assert len(question.choices) == 0

# 3. Testar se uma exceção é lançada ao tentar remover um ID inexistente
def test_remove_invalid_choice_id_raises_exception():
    question = Question(title='Q1')
    question.add_choice('A')
    with pytest.raises(Exception, match='Invalid choice id'):
        question.remove_choice_by_id(99)

# 4. Testar a remoção de todas as escolhas de uma vez
def test_remove_all_choices():
    question = Question(title='Q1')
    question.add_choice('A')
    question.add_choice('B')
    question.remove_all_choices()
    assert len(question.choices) == 0

# 5. Testar a definição de escolhas corretas através de uma lista de IDs
def test_set_correct_choices():
    question = Question(title='Q1')
    question.add_choice('A', False)
    question.add_choice('B', False)
    question.set_correct_choices([1, 2])
    assert question.choices[0].is_correct is True
    assert question.choices[1].is_correct is True

# 6. Testar o método de corrigir escolhas (retorna apenas os IDs corretos)
def test_correct_selected_choices():
    question = Question(title='Q1', max_selections=2)
    question.add_choice('A', True)  # ID 1 (Correta)
    question.add_choice('B', False) # ID 2 (Incorreta)
    
    # Se o usuário selecionar 1 e 2, apenas o 1 está certo
    correct_ids = question.correct_selected_choices([1, 2])
    assert correct_ids == [1]

# 7. Testar se o limite de max_selections bloqueia tentativas excessivas
def test_correct_selected_choices_exceeds_max_selections():
    question = Question(title='Q1', max_selections=1)
    question.add_choice('A')
    question.add_choice('B')
    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([1, 2])

# 8. Testar a validação de pontos (não pode ser menor que 1)
def test_question_invalid_points_raises_exception():
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='Q1', points=0)

# 9. Testar a validação de limite de caracteres do título da questão (>200)
def test_question_title_length_limit():
    long_title = 'A' * 201
    with pytest.raises(Exception, match='Title cannot be longer than 200 characters'):
        Question(title=long_title)

# 10. Testar a validação de texto vazio ao adicionar uma escolha
def test_choice_empty_text_raises_exception():
    question = Question(title='Q1')
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')