// ============================== Criando os nós ==============================

// Alunos
CREATE (:Aluno {nome: 'Ana Silva', matricula: '2024001', email: 'ana.silva@email.com', idade: 21});
CREATE (:Aluno {nome: 'Bruno Souza', matricula: '2024002', email: 'bruno.souza@email.com', idade: 23});
CREATE (:Aluno {nome: 'Carla Mendes', matricula: '2024003', email: 'carla.mendes@email.com', idade: 20});
CREATE (:Aluno {nome: 'Diego Lima', matricula: '2024004', email: 'diego.lima@email.com', idade: 25});

// Cursos
CREATE (:Curso {nome: 'Ciência da Computação', duracao: 8});
CREATE (:Curso {nome: 'Sistemas de Informação', duracao: 8});
CREATE (:Curso {nome: 'Engenharia de Software', duracao: 10});

// Grupos de Estudos
CREATE (:GrupoEstudo {nome: 'Grupo Algoritmos'});
CREATE (:GrupoEstudo {nome: 'Grupo Banco de Dados'});
CREATE (:GrupoEstudo {nome: 'Grupo IA'});


// ============================== Criando Relacionamentos ==============================

// Alunos -> Cursos

MATCH (a:Aluno {matricula: '2024001'}), (c:Curso {nome: 'Ciência da Computação'})
CREATE (a)-[:MATRICULADO_EM]->(c);

MATCH (a:Aluno {matricula: '2024002'}), (c:Curso {nome: 'Sistemas de Informação'})
CREATE (a)-[:MATRICULADO_EM]->(c);

MATCH (a:Aluno {matricula: '2024003'}), (c:Curso {nome: 'Engenharia de Software'})
CREATE (a)-[:MATRICULADO_EM]->(c);

MATCH (a:Aluno {matricula: '2024004'}), (c:Curso {nome: 'Ciência da Computação'})
CREATE (a)-[:MATRICULADO_EM]->(c);

// Alunos -> Grupos de Estudos
MATCH (a:Aluno {matricula: '2024001'}), (g:GrupoEstudo {nome: 'Grupo Algoritmos'})
CREATE (a)-[:PARTICIPA_DE]->(g);

MATCH (a:Aluno {matricula: '2024001'}), (g:GrupoEstudo {nome: 'Grupo IA'})
CREATE (a)-[:PARTICIPA_DE]->(g);

MATCH (a:Aluno {matricula: '2024002'}), (g:GrupoEstudo {nome: 'Grupo Banco de Dados'})
CREATE (a)-[:PARTICIPA_DE]->(g);

MATCH (a:Aluno {matricula: '2024003'}), (g:GrupoEstudo {nome: 'Grupo IA'})
CREATE (a)-[:PARTICIPA_DE]->(g);

MATCH (a:Aluno {matricula: '2024004'}), (g:GrupoEstudo {nome: 'Grupo Algoritmos'})
CREATE (a)-[:PARTICIPA_DE]->(g);

// Cursos -> Grupos de Estudos
MATCH (c:Curso {nome: 'Ciência da Computação'}), (g:GrupoEstudo {nome: 'Grupo Algoritmos'})
CREATE (c)-[:POSSUI_GRUPO]->(g);

MATCH (c:Curso {nome: 'Ciência da Computação'}), (g:GrupoEstudo {nome: 'Grupo IA'})
CREATE (c)-[:POSSUI_GRUPO]->(g);

MATCH (c:Curso {nome: 'Sistemas de Informação'}), (g:GrupoEstudo {nome: 'Grupo Banco de Dados'})
CREATE (c)-[:POSSUI_GRUPO]->(g);

// ============================== Vizualizar os grafos ==============================

// Ver todos os nós e relacionamentos
MATCH (n) RETURN n;

// Ver alunos com seus cursos
MATCH (a:Aluno)-[:MATRICULADO_EM]->(c:Curso)
RETURN a.nome, a.matricula, c.nome AS curso;

// Ver alunos e seus grupos de estudo
MATCH (a:Aluno)-[:PARTICIPA_DE]->(g:GrupoEstudo)
RETURN a.nome, collect(g.nome) AS grupos;
