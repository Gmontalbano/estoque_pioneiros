import streamlit as st
import json
from PIL import Image



def write_json(dictionary, file_):
    with open(f"{file_}", "w") as outfile:
        json.dump(dictionary, outfile)


def read_json(file):
    with open(f'{file}', 'r') as openfile:
        return json.load(openfile)


def main_page():
    image = Image.open('logo.jpg')

    st.image(image, caption='Mais que um clube, uma família',width=200)
    st.markdown("# Estoque de especialidades e classes ")
    st.sidebar.markdown("# Início")
    st.sidebar.markdown("Um dia essa página vai ficar bonita ")


def page2():
    st.sidebar.markdown("# Entradas e saídas de especialidades e classes")
    st.sidebar.markdown("Apenas para atualizar o valor de estoque, caso não tenha a opção desejada é necessário fazer o cadastro na aba cadastro")

    classes = read_json('classes.json')
    especialidades = read_json('especialidades.json')

    st.title(f'Controle de Especialidades & Classes')

    #  classes
    menu = st.selectbox('Menu', ('select', 'Classes', 'Especialidades'))

    if menu == 'Classes':
        option = st.selectbox('Classes', (x for x in classes))
        #  st.write('Estoque:', classes[option])
        st.metric(label="Estoque", value=classes[option])
        if classes[option] <= 0:
            st.error("SEM ESTOQUE")
        with st.form("my_form"):
            qtd = st.number_input('Insert a number')

            if classes[option] < 0:
                classes[option] = 0

            adicionar = st.form_submit_button("Adicionar")
            retirar = st.form_submit_button("Retirar")

            if retirar:
                classes[option] = classes[option] - qtd
                write_json(classes, 'classes.json')
                st.experimental_rerun()
            if adicionar:
                classes[option] = classes[option] + qtd
                write_json(classes, 'classes.json')
                st.experimental_rerun()

    elif menu == 'Especialidades':
        option = st.selectbox('Especialidades', (x for x in especialidades))
        st.metric(label="Estoque", value=especialidades[option])

        if especialidades[option] <= 0:
            st.error("SEM ESTOQUE")

        with st.form("my_form"):
            qtd = st.number_input('Insert a number')

            if especialidades[option] < 0:
                especialidades[option] = 0

            adicionar = st.form_submit_button("Adicionar")
            subtrair = st.form_submit_button("Retirar")

            if subtrair:
                especialidades[option] = especialidades[option] - qtd
                write_json(especialidades, 'especialidades.json')
                st.experimental_rerun()
            if adicionar:
                especialidades[option] = especialidades[option] + qtd
                write_json(especialidades, 'especialidades.json')
                st.experimental_rerun()


def page3():
    st.sidebar.markdown("# Cadastro de novas especialidades e classes")
    st.sidebar.markdown("Apenas para colocar especialidades que não tinhamos cadastradas ou remover especialidades que não existem mais")

    classes = read_json('classes.json')
    especialidades = read_json('especialidades.json')

    st.title(f'Cadastro de Especialidades & Classes')

    menu = st.selectbox('Menu', ('select', 'Classes', 'Especialidades'))

    if menu == 'Classes':

        option_to_do = st.selectbox('Cadastrar - Remover', ('select', 'Cadastrar', 'Remover'))

        if option_to_do == 'Cadastrar':
            with st.form("cadastrar"):
                st.markdown("## Cadastrar")
                especialidade = st.text_input('Classe')
                number = st.number_input('Quantidade')
                cadastro = st.form_submit_button("Cadastrar")
                if cadastro:
                    classes[especialidade] = number
                    write_json(classes, 'classes.json')
                    st.experimental_rerun()

            st.markdown("### Confirmar")
            st.selectbox('Classes', (x for x in classes))

        if option_to_do == 'Remover':
            with st.form("Remover"):
                st.markdown("## Remover")
                option = st.selectbox('Classe', (x for x in especialidades))
                remove = st.form_submit_button("Remover")
                if remove:
                    classes.pop(option)
                    write_json(classes, 'classes.json')
                    st.experimental_rerun()
            st.markdown("### Confirmar")
            st.selectbox('Classes', (x for x in classes))

    if menu == 'Especialidades':

        option_to_do = st.selectbox('Cadastrar - Remover', ('select', 'Cadastrar', 'Remover'))
        if option_to_do == 'Cadastrar':
            with st.form("cadastrar"):
                st.markdown("## Cadastrar")
                especialidade = st.text_input('Especialidade')
                especialidade = especialidade.title()
                number = st.number_input('Quantidade')
                cadastro = st.form_submit_button("Cadastrar")
                if cadastro:
                    especialidades[especialidade] = number
                    x = {}
                    x = especialidades
                    especialidades = json.dumps(x, sort_keys=True)
                    especialidades = eval(especialidades)
                    write_json(especialidades, 'especialidades.json')
                    st.experimental_rerun()

            st.markdown("### Confirmar")
            st.selectbox('especialidades', (x for x in especialidades))

        if option_to_do == 'Remover':
            with st.form("Remover"):
                st.markdown("## Remover")
                option = st.selectbox('especialidades', (x for x in especialidades))
                remove = st.form_submit_button("Remover")
                if remove:
                    especialidades.pop(option)
                    write_json(especialidades, 'especialidades.json')
                    st.experimental_rerun()
            st.markdown("### Confirmar")
            st.selectbox('especialidades', (x for x in especialidades))


if __name__ == "__main__":
    st.set_page_config(page_title='Pioneiros da Colina',layout="wide",page_icon='logo.jpg')
    page_names_to_funcs = {
        "Início": main_page,
        "Entradas e saídas": page2,
        "Cadastro": page3,
    }

    selected_page = st.sidebar.selectbox("Navegação", page_names_to_funcs.keys())
    page_names_to_funcs[selected_page]()

