import streamlit as st
from crud_operations import Neo4jCRUD
from models import Person, Relationship
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Neo4j Dashboard",
    page_icon=":bar_chart:",
    layout="wide"
)

st.title("📊 Dashboard Interativa Neo4j")
st.markdown("""
    Gerencie seu banco de dados Neo4j através desta interface amigável.
    Todas as operações CRUD estão disponíveis abaixo.
""")

with st.sidebar:
    st.header("🔌 Configuração de Conexão")
    if 'db' not in st.session_state:
        try:
            st.session_state.db = Neo4jCRUD()
            st.success("Conectado ao Neo4j Sandbox!")
        except Exception as e:
            st.error(f"Erro na conexão: {str(e)}")
    
    st.markdown("---")
    st.markdown("### Operações Básicas")
    operation = st.radio(
        "Selecione a operação:",
        ["Visualizar Dados", "Adicionar Pessoa", "Editar Pessoa", "Remover Pessoa", "Relacionamentos"]
    )

if 'db' in st.session_state:
    db = st.session_state.db
    
    if operation == "Visualizar Dados":
        st.header("👥 Pessoas no Banco de Dados")
        
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.slider("Idade mínima", 18, 100, 18)
        with col2:
            profession_filter = st.text_input("Filtrar por profissão")
        

        people = db.get_all_people()
        filtered_people = [
            p for p in people 
            if p.age >= min_age and 
            (profession_filter.lower() in p.profession.lower() if profession_filter else True)
        ]

        if filtered_people:
            df = pd.DataFrame([p.to_dict() for p in filtered_people])
            st.dataframe(df, use_container_width=True)

            st.subheader("📈 Distribuição por Profissão")
            profession_counts = df['profession'].value_counts().reset_index()
            profession_counts.columns = ['Profissão', 'Quantidade']
            
            fig = px.bar(
                profession_counts, 
                x='Profissão', 
                y='Quantidade',
                color='Profissão',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Nenhuma pessoa encontrada com esses filtros!")

    elif operation == "Adicionar Pessoa":
        st.header("➕ Adicionar Nova Pessoa")
        
        with st.form("add_person_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nome*", placeholder="João Silva")
            with col2:
                age = st.number_input("Idade*", min_value=1, max_value=120, value=30)
            
            profession = st.text_input("Profissão*", placeholder="Engenheiro")
            email = st.text_input("Email", placeholder="joao@email.com")
            
            submitted = st.form_submit_button("Adicionar Pessoa")
            if submitted:
                if name and profession:
                    person = Person(name, age, profession, email)
                    result = db.create_person(person)
                    if result:
                        st.success(f"Pessoa {name} adicionada com sucesso!")
                    else:
                        st.error("Erro ao adicionar pessoa!")
                else:
                    st.warning("Campos obrigatórios* não preenchidos!")

    elif operation == "Editar Pessoa":
        st.header("✏️ Editar Pessoa Existente")
        
        people = db.get_all_people()
        if people:
            person_names = [p.name for p in people]
            selected_name = st.selectbox("Selecione a pessoa para editar", person_names)
            
            selected_person = next(p for p in people if p.name == selected_name)
            
            with st.form("edit_person_form"):
                st.write(f"Editando: {selected_person.name}")
                
                col1, col2 = st.columns(2)
                with col1:
                    new_age = st.number_input("Idade", value=selected_person.age)
                with col2:
                    new_profession = st.text_input("Profissão", value=selected_person.profession)
                
                new_email = st.text_input("Email", value=selected_person.email or "")
                
                submitted = st.form_submit_button("Atualizar Pessoa")
                if submitted:
                    updates = {
                        "age": new_age,
                        "profession": new_profession,
                        "email": new_email if new_email else None
                    }
                    result = db.update_person(selected_name, updates)
                    if result:
                        st.success(f"Pessoa {selected_name} atualizada!")
                    else:
                        st.error("Erro ao atualizar pessoa!")
        else:
            st.warning("Nenhuma pessoa encontrada no banco de dados!")

    elif operation == "Remover Pessoa":
        st.header("🗑️ Remover Pessoa")
        
        people = db.get_all_people()
        if people:
            person_names = [p.name for p in people]
            selected_name = st.selectbox("Selecione a pessoa para remover", person_names)
            
            if st.button("Confirmar Remoção"):
                if db.delete_person(selected_name):
                    st.success(f"Pessoa {selected_name} removida com sucesso!")
                    st.experimental_rerun()  
                else:
                    st.error("Erro ao remover pessoa!")
        else:
            st.warning("Nenhuma pessoa encontrada no banco de dados!")
    
    elif operation == "Relacionamentos":
        st.header("🤝 Gerenciar Relacionamentos")
        
        tab1, tab2 = st.tabs(["Criar Relacionamento", "Visualizar Relacionamentos"])
        
        with tab1:
            st.subheader("Criar Novo Relacionamento")
            people = db.get_all_people()
            
            if len(people) >= 2:
                col1, col2 = st.columns(2)
                with col1:
                    from_person = st.selectbox("De:", [p.name for p in people])
                with col2:
                    to_person = st.selectbox("Para:", [p.name for p in people if p.name != from_person])
                
                rel_type = st.selectbox("Tipo de relacionamento:", ["KNOWS", "WORKS_WITH", "FRIENDS_WITH"])
                since = st.number_input("Desde (ano):", min_value=1900, max_value=2100, value=2023)
                
                if st.button("Criar Relacionamento"):
                    rel = Relationship(rel_type, {"since": since})
                    if db.create_relationship(from_person, to_person, rel):
                        st.success(f"Relacionamento criado: {from_person} → {to_person}")
                    else:
                        st.error("Erro ao criar relacionamento!")
            else:
                st.warning("Você precisa de pelo menos 2 pessoas no banco para criar relacionamentos!")
        
        with tab2:
            st.subheader("Visualizar Relacionamentos")
            people = db.get_all_people()
            
            if people:
                selected_person = st.selectbox("Selecione uma pessoa:", [p.name for p in people])
                
                relationships = db.get_relationships(selected_person)
                if relationships:
                    st.write(f"Relacionamentos de {selected_person}:")
                    for rel in relationships:
                        st.write(f"- {rel['type']} → {rel['name']} (desde {rel['props'].get('since', '?')})")
 
                    nodes = {selected_person: "Pessoa Selecionada"}
                    links = []
                    
                    for rel in relationships:
                        nodes[rel['name']] = "Conhecido"
                        links.append({
                            "source": selected_person,
                            "target": rel['name'],
                            "type": rel['type']
                        })

                    nodes_df = pd.DataFrame({
                        "name": list(nodes.keys()),
                        "type": list(nodes.values())
                    })
                    
                    links_df = pd.DataFrame(links)
                    
                    fig = px.scatter(
                        nodes_df, 
                        x=[1] * len(nodes_df),  
                        y=[1] * len(nodes_df),  
                        text="name",
                        color="type",
                        title=f"Rede de Relacionamentos de {selected_person}"
                    )
                    
                    for _, link in links_df.iterrows():
                        fig.add_shape(
                            type="line",
                            x0=1, y0=1,
                            x1=1, y1=1,
                            line=dict(color="gray", width=1),
                            xref="x", yref="y"
                        )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"{selected_person} não tem relacionamentos registrados.")
            else:
                st.warning("Nenhuma pessoa encontrada no banco de dados!")

else:
    st.error("Não foi possível conectar ao banco de dados. Verifique as configurações.")