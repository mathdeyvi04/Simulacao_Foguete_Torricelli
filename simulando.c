#include <stdio.h>
#include <stdlib.h>
#include <locale.h>
#include <math.h>


// Nomeando algumas constantes
#define DELTA_TEMPO 0.00001
#define G 9.81
#define LOCAL "C:\\Users\\deyvi\\Documents\\ImperioPy\\Divers�o\\Simula��oVisualFogueteTorricelli\\dados.txt"
#define u 0.15

// Criando nosso corpo completo
typedef struct _ {
	
	double B;  // Coeficiente do Sistema
	double Y;  // Raz�o entre �reas
	double h;  // Altura do L�quido
	
	double a;  // Gravidade Efetiva


	// Vari�veis Cin�maticas
	double pos;
	double vel;
	double acel;
	
} Foguete ;


double obtendo_acel_inst(
	Foguete corpo
){
	/*
	Descri��o:
		Fun��o respons�vel por, a partir dos valores inst�ntaneos, calcular a acelera��o
		do foguete.
		
	Par�metros:
		corpo -> vari�vel que cont�m todos os dados
		
	Retorno:
		Acelera��o Inst�ntanea
	*/
	
	return corpo.a * ( corpo.h / ( corpo.B + corpo.h )) - G * u;
}


double derramando_liquido(
	Foguete corpo
){
	/*
	Descri��o:
		Fun��o respons�vel por reduzir a quantidade de l�quido dentro
		do reservat�rio.

	Par�metros:
		Foguete

	Retorno:
		Nova altura do l�quido que dever� ser menor
	*/
	
	if(corpo.h <= 0){
		return 0;
	}
	
	return corpo.h - sqrt(corpo.a * corpo.Y * corpo.h) * DELTA_TEMPO;
}


void salvando_dados(
	double instante,
	Foguete corpo,
	FILE *arquivo
){
	/*
	Descri��o:
		Fun��o respons�vel por salvar os dados de uma vez dentro do arquivo,
		reduzindo o tempo de execu��o.
		
	Par�metros:
		t,
		Informa��es do Corpo,
		Arquivo em que ser�o salvas
		
	Retorno:
		Caracter�sticas inst�ntaneas do sistema salvas.
	*/
	
	if(instante == 0){
		fprintf(
			arquivo,
			"%.6lf,%.6lf,%.6lf, %.6lf",
			instante,
			corpo.pos,
			corpo.vel,
			corpo.h
		);
		
	}else{
		fprintf(
			arquivo,
			"\n%.6lf,%.6lf,%.6lf, %.6lf",
			instante,
			corpo.pos,
			corpo.vel,
			corpo.h
		);
	}
	
}


int main(){
	
	setlocale(LC_ALL, "Portuguese");
	setlocale(LC_NUMERIC, "C");
	
	// Devemos criar nosso foguete.
	Foguete foguete;
	
	// Preencher as informa��es iniciais
	printf("Insira o coeficiente B do sistema(B): ");
	scanf("%lf", &foguete.B);
	getchar();
	
	printf("\nInsira a altura inicial do l�quido(h): ");
	scanf("%lf", &foguete.h);
	getchar();
	
	// Vamos definir o gamma como sendo uma constante fixa tamb�m
	foguete.Y = 0.1;
	
	// Vamos definir uma constante de acelera��o
	foguete.a = (2 * G * foguete.Y) / (1 - ((foguete.Y * foguete.Y)));
	
	// Dando algumas informa��es
	printf(
		"\nTempo Total At� Fim da Propuls�o: %.3lf s",
		sqrt(4 * foguete.h / (foguete.Y * foguete.a))
	);
	
	// Devemos fazer o estudo das condicionais
	if (u != 0){
		// Caso haja atrito.
		
		if(foguete.h < (
			foguete.B / ((foguete.a / (u * G)) - 1)
		)){
			printf("\nO foguete nem sai do lugar devido � baixa altura de l�quido.");
			printf("\n\nEncerrado Sem Sucesso");
			return 0;
		}
		
		if(foguete.Y < sqrt(1 + (1 / (u * u))) - (1 / u)){
			printf("\nO foguete nunca sair� do lugar devido � altura m�nima ser INFINITA.");
			printf("\n\nEncerrado Sem Sucesso");
			return 0;
		}
	}
	
	
	// Criar o arquivo que manter� as informa��es
	FILE *ARQUIVO = fopen(LOCAL, "w");
	
	// Agora devemos rodar a simula��o
	double tempo_total = 0;
	while(foguete.vel > 0){
		
		// Devemos calcular acelera��o.
		foguete.acel = obtendo_acel_inst(foguete);
		
		// Reduzir o valor da altura do l�quido
		foguete.h = derramando_liquido(foguete);
		
		// Aplicar a cinem�tica
		foguete.vel = foguete.vel + foguete.acel * DELTA_TEMPO;
		foguete.pos = foguete.pos + foguete.vel * DELTA_TEMPO + 0.5 * foguete.acel * DELTA_TEMPO * DELTA_TEMPO;
		
		// E finalmente salvar os dados
		salvando_dados(tempo_total, foguete, ARQUIVO);
		
		tempo_total = tempo_total + DELTA_TEMPO;
	}
	
	fclose(ARQUIVO);

	printf("\n\n\nEncerrei com sucesso");
	return 0;
}
