.data
.balign 8
AUX_ZERO: .double 0.0
.balign 8
AUX_ONE: .double 1.0
.balign 8
AUX_TEN: .double 10.0
.balign 8
TMP_Q: .double 0.0
.balign 8
TMP_A: .double 0.0
.balign 8
TMP_B: .double 0.0
.balign 8
TMP_BASE: .double 0.0
.balign 8
TMP_RES: .double 0.0
.balign 4
TMP_EXP_I: .word 0
.balign 4
AUX_INTBUF: .word 0
.balign 8
CONST_0: .double 2.60
.balign 8
CONST_1: .double 1.4
.balign 8
CONST_2: .double 10.0
.balign 8
CONST_3: .double 3
.balign 8
CONST_4: .double 2
.balign 8
CONST_5: .double 4
.balign 8
CONST_6: .double 8
.balign 8
CONST_7: .double 2.0
.balign 8
CONST_8: .double 9
.balign 8
CONST_9: .double 1
.balign 8
CONST_10: .double 5
.balign 8
CONST_11: .double 0
.balign 8
CONST_12: .double 12.0
.balign 8
MEM_X: .double 0.0
.balign 8
RES_0: .double 0.0
.balign 8
RES_1: .double 0.0
.balign 8
RES_2: .double 0.0
.balign 8
RES_3: .double 0.0
.balign 8
RES_4: .double 0.0
.balign 8
RES_5: .double 0.0
.balign 8
RES_6: .double 0.0
.balign 8
RES_7: .double 0.0
.balign 8
RES_8: .double 0.0
.balign 8
RES_9: .double 0.0
.balign 8
TEMP_0: .double 0.0
.balign 8
TEMP_1: .double 0.0
.balign 8
TEMP_2: .double 0.0
.balign 8
TEMP_3: .double 0.0
.balign 8
TEMP_4: .double 0.0
.balign 8
TEMP_5: .double 0.0
.balign 8
TEMP_6: .double 0.0
.balign 8
TEMP_7: .double 0.0
.balign 8
TEMP_8: .double 0.0
.balign 8
TEMP_9: .double 0.0
.balign 8
TEMP_10: .double 0.0
.balign 8
TEMP_11: .double 0.0
.balign 8
TEMP_12: .double 0.0
.balign 8
TEMP_13: .double 0.0
.balign 8
TEMP_14: .double 0.0
.balign 8
TEMP_15: .double 0.0
.balign 8
TEMP_16: .double 0.0
SEG_TAB: .byte 0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F
.syntax unified

.text
.global _start

_start:
    @ ===== LINHA 1 =====
    @ operacao VADD.F64
    LDR R0, =CONST_0
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_1
    VLDR.F64 D1, [R1]
    VADD.F64 D0, D0, D1
    LDR R2, =TEMP_0
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_0
    VLDR.F64 D0, [R0]
    LDR R1, =RES_0
    VSTR.F64 D0, [R1]

    @ ===== LINHA 2 =====
    @ escrita memoria MEM_X
    LDR R0, =CONST_2
    VLDR.F64 D0, [R0]
    LDR R1, =MEM_X
    VSTR.F64 D0, [R1]
    LDR R2, =TEMP_1
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_1
    VLDR.F64 D0, [R0]
    LDR R1, =RES_1
    VSTR.F64 D0, [R1]

    @ ===== LINHA 3 =====
    @ leitura memoria MEM_X
    LDR R0, =MEM_X
    VLDR.F64 D0, [R0]
    LDR R1, =TEMP_2
    VSTR.F64 D0, [R1]
    LDR R0, =TEMP_2
    VLDR.F64 D0, [R0]
    LDR R1, =RES_2
    VSTR.F64 D0, [R1]

    @ ===== LINHA 4 =====
    @ operacao VADD.F64
    LDR R0, =CONST_3
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_4
    VLDR.F64 D1, [R1]
    VADD.F64 D0, D0, D1
    LDR R2, =TEMP_3
    VSTR.F64 D0, [R2]
    @ operacao VMUL.F64
    LDR R0, =TEMP_3
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_5
    VLDR.F64 D1, [R1]
    VMUL.F64 D0, D0, D1
    LDR R2, =TEMP_4
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_4
    VLDR.F64 D0, [R0]
    LDR R1, =RES_3
    VSTR.F64 D0, [R1]

    @ ===== LINHA 5 =====
    @ operacao VSUB.F64
    LDR R0, =CONST_2
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_3
    VLDR.F64 D1, [R1]
    VSUB.F64 D0, D0, D1
    LDR R2, =TEMP_5
    VSTR.F64 D0, [R2]
    @ operacao VDIV.F64
    LDR R0, =TEMP_5
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_4
    VLDR.F64 D1, [R1]
    VDIV.F64 D0, D0, D1
    LDR R2, =TEMP_6
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_6
    VLDR.F64 D0, [R0]
    LDR R1, =RES_4
    VSTR.F64 D0, [R1]

    @ ===== LINHA 6 =====
    @ operacao INTEGER_DIV_64 chama funcao
    LDR R0, =CONST_6
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_3
    VLDR.F64 D1, [R1]
    BL INTEGER_DIV_64
    LDR R2, =TEMP_7
    VSTR.F64 D0, [R2]
    @ operacao VADD.F64
    LDR R0, =TEMP_7
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_7
    VLDR.F64 D1, [R1]
    VADD.F64 D0, D0, D1
    LDR R2, =TEMP_8
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_8
    VLDR.F64 D0, [R0]
    LDR R1, =RES_5
    VSTR.F64 D0, [R1]

    @ ===== LINHA 7 =====
    @ operacao MODULO_64 chama funcao
    LDR R0, =CONST_8
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_5
    VLDR.F64 D1, [R1]
    BL MODULO_64
    LDR R2, =TEMP_9
    VSTR.F64 D0, [R2]
    @ operacao VADD.F64
    LDR R0, =TEMP_9
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_9
    VLDR.F64 D1, [R1]
    VADD.F64 D0, D0, D1
    LDR R2, =TEMP_10
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_10
    VLDR.F64 D0, [R0]
    LDR R1, =RES_6
    VSTR.F64 D0, [R1]

    @ ===== LINHA 8 =====
    @ operacao EXPONENTIATION_64 chama funcao
    LDR R0, =CONST_7
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_3
    VLDR.F64 D1, [R1]
    BL EXPONENTIATION_64
    LDR R2, =TEMP_11
    VSTR.F64 D0, [R2]
    @ operacao VSUB.F64
    LDR R0, =TEMP_11
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_9
    VLDR.F64 D1, [R1]
    VSUB.F64 D0, D0, D1
    LDR R2, =TEMP_12
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_12
    VLDR.F64 D0, [R0]
    LDR R1, =RES_7
    VSTR.F64 D0, [R1]

    @ ===== LINHA 9 =====
    @ operacao VADD.F64
    LDR R0, =MEM_X
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_10
    VLDR.F64 D1, [R1]
    VADD.F64 D0, D0, D1
    LDR R2, =TEMP_13
    VSTR.F64 D0, [R2]
    @ operacao VMUL.F64
    LDR R0, =TEMP_13
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_4
    VLDR.F64 D1, [R1]
    VMUL.F64 D0, D0, D1
    LDR R2, =TEMP_14
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_14
    VLDR.F64 D0, [R0]
    LDR R1, =RES_8
    VSTR.F64 D0, [R1]

    @ ===== LINHA 10 =====
    @ RES leitura de histórico linha RES_8
    LDR R0, =RES_8
    VLDR.F64 D0, [R0]
    LDR R1, =TEMP_15
    VSTR.F64 D0, [R1]
    @ operacao VADD.F64
    LDR R0, =TEMP_15
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_12
    VLDR.F64 D1, [R1]
    VADD.F64 D0, D0, D1
    LDR R2, =TEMP_16
    VSTR.F64 D0, [R2]
    LDR R0, =TEMP_16
    VLDR.F64 D0, [R0]
    LDR R1, =RES_9
    VSTR.F64 D0, [R1]

      LDR R0, =RES_9
      VLDR.F64 D0, [R0]
      BL DISPLAY_RESULT_7SEG_1DP
    @ fim do programa
FIM:
    B FIM

@ ===== ROTINA INTEGER_DIV_64 =====
INTEGER_DIV_64:
    @ entrada: D0 = A, D1 = B
    @ saida:   D0 = A // B

    @ se B == 0.0, retorna 0.0
    VCMP.F64 D1, #0.0
    VMRS APSR_nzcv, FPSCR
    BEQ INTEGER_DIV_64_DIV_ZERO

    @ q_real = A / B
    VDIV.F64 D2, D0, D1

    @ q_trunc_i = trunc(q_real) em inteiro assinado
    VCVT.S32.F64 S6, D2

    @ q_trunc = double(q_trunc_i)
    VCVT.F64.S32 D3, S6

    @ se q_real == q_trunc, terminou
    VCMP.F64 D2, D3
    VMRS APSR_nzcv, FPSCR
    BEQ INTEGER_DIV_64_DONE

    @ se q_real >= 0, truncamento ja coincide com floor
    VCMP.F64 D2, #0.0
    VMRS APSR_nzcv, FPSCR
    BGE INTEGER_DIV_64_DONE

    @ caso negativo com parte fracionaria: floor = trunc - 1.0
    LDR R0, =AUX_ONE
    VLDR.F64 D4, [R0]
    VSUB.F64 D3, D3, D4

INTEGER_DIV_64_DONE:
    LDR R0, =TMP_Q
    VSTR.F64 D3, [R0]
    VLDR.F64 D0, [R0]
    BX LR

INTEGER_DIV_64_DIV_ZERO:
    LDR R0, =AUX_ZERO
    VLDR.F64 D0, [R0]
    BX LR

@ ===== ROTINA MODULO_64 =====
MODULO_64:
    @ entrada: D0 = A, D1 = B
    @ saida:   D0 = A % B

    PUSH {LR}

    @ se B == 0.0, retorna 0.0
    VCMP.F64 D1, #0.0
    VMRS APSR_nzcv, FPSCR
    BEQ MODULO_64_DIV_ZERO

    @ guarda A e B em memoria
    LDR R0, =TMP_A
    VSTR.F64 D0, [R0]
    LDR R0, =TMP_B
    VSTR.F64 D1, [R0]

    @ q = A // B
    BL INTEGER_DIV_64

    @ recarrega B
    LDR R0, =TMP_B
    VLDR.F64 D7, [R0]

    @ D2 = q * B
    VMUL.F64 D2, D0, D7

    @ recarrega A
    LDR R0, =TMP_A
    VLDR.F64 D6, [R0]

    @ r = A - q * B
    VSUB.F64 D0, D6, D2

    POP {LR}
    BX LR

MODULO_64_DIV_ZERO:
    LDR R0, =AUX_ZERO
    VLDR.F64 D0, [R0]
    POP {LR}
    BX LR

@ ===== ROTINA EXPONENTIATION_64 =====
EXPONENTIATION_64:
    @ entrada: D0 = base, D1 = expoente
    @ saida:   D0 = base ^ expoente
    @ esta versao aceita apenas expoente inteiro nao negativo

    @ se expoente < 0.0, retorna 0.0
    VCMP.F64 D1, #0.0
    VMRS APSR_nzcv, FPSCR
    BLT EXPONENTIATION_64_INVALID

    @ converte expoente para inteiro truncado
    VCVT.S32.F64 S8, D1
    VCVT.F64.S32 D3, S8

    @ se expoente original != expoente inteiro, invalido
    VCMP.F64 D1, D3
    VMRS APSR_nzcv, FPSCR
    BNE EXPONENTIATION_64_INVALID

    @ move contador inteiro para registrador ARM via memoria
    LDR R0, =TMP_EXP_I
    VSTR S8, [R0]
    LDR R4, [R0]

    @ resultado = 1.0
    LDR R0, =AUX_ONE
    VLDR.F64 D4, [R0]

    @ guarda base via memoria
    LDR R0, =TMP_BASE
    VSTR.F64 D0, [R0]
    VLDR.F64 D5, [R0]

EXPONENTIATION_64_LOOP_CHECK:
    CMP R4, #0
    BEQ EXPONENTIATION_64_DONE

    VMUL.F64 D4, D4, D5
    SUB R4, R4, #1
    B EXPONENTIATION_64_LOOP_CHECK

EXPONENTIATION_64_DONE:
    LDR R0, =TMP_RES
    VSTR.F64 D4, [R0]
    VLDR.F64 D0, [R0]
    BX LR

EXPONENTIATION_64_INVALID:
    LDR R0, =AUX_ZERO
    VLDR.F64 D0, [R0]
    BX LR

@ ===== ROTINA GET_SEG_DIGIT =====
GET_SEG_DIGIT:
    @ entrada: R0 = digito (0..9)
    @ saida:   R0 = padrao do 7 segmentos
    PUSH {R1, LR}
    LDR R1, =SEG_TAB
    LDRB R0, [R1, R0]
    POP {R1, LR}
    BX LR

@ ===== ROTINA DIVMOD10_U32 =====
DIVMOD10_U32:
    @ entrada: R0 = valor
    @ saida:   R0 = quociente, R1 = resto
    PUSH {R2, LR}
    MOV R2, #0

DIVMOD10_U32_LOOP:
    CMP R0, #10
    BLT DIVMOD10_U32_DONE
    SUB R0, R0, #10
    ADD R2, R2, #1
    B DIVMOD10_U32_LOOP

DIVMOD10_U32_DONE:
    MOV R1, R0
    MOV R0, R2
    POP {R2, LR}
    BX LR

@ ===== ROTINA DISPLAY_RESULT_7SEG_1DP =====
DISPLAY_RESULT_7SEG_1DP:
    @ entrada: D0 = valor final
    PUSH {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, LR}

    @ sinal
    MOV R9, #0
    VCMP.F64 D0, #0.0
    VMRS APSR_nzcv, FPSCR
    BGE DISPLAY_RESULT_7SEG_POSITIVE
    MOV R9, #0x40
    VNEG.F64 D0, D0

DISPLAY_RESULT_7SEG_POSITIVE:
    @ escala por 10
    LDR R0, =AUX_TEN
    VLDR.F64 D1, [R0]
    VMUL.F64 D0, D0, D1

    @ converte para inteiro
    VCVT.U32.F64 S0, D0
    LDR R0, =AUX_INTBUF
    VSTR S0, [R0]
    LDR R4, [R0]

    @ separa parte inteira e decimal
    MOV R0, R4
    BL DIVMOD10_U32
    MOV R5, R0      @ parte inteira
    MOV R6, R1      @ decimal

    @ separa unidades, dezenas e centenas
    MOV R0, R5
    BL DIVMOD10_U32
    MOV R5, R1      @ unidades
    MOV R7, R0      @ dezenas+centenas

    MOV R0, R7
    BL DIVMOD10_U32
    MOV R8, R1      @ dezenas
    MOV R7, R0      @ centenas

    @ converte decimal
    MOV R0, R6
    BL GET_SEG_DIGIT
    MOV R6, R0

    @ converte unidades (sempre mostra)
    MOV R0, R5
    BL GET_SEG_DIGIT
    MOV R5, R0

    @ converte dezenas:
    @ mostra se centenas != 0 OU dezenas != 0
    CMP R7, #0
    BNE DISPLAY_RESULT_7SEG_SHOW_TENS
    CMP R8, #0
    BNE DISPLAY_RESULT_7SEG_SHOW_TENS
    MOV R8, #0
    B DISPLAY_RESULT_7SEG_TENS_DONE

DISPLAY_RESULT_7SEG_SHOW_TENS:
    MOV R0, R8
    BL GET_SEG_DIGIT
    MOV R8, R0

DISPLAY_RESULT_7SEG_TENS_DONE:
    @ converte centenas ou deixa branco
    CMP R7, #0
    BEQ DISPLAY_RESULT_7SEG_HUNDREDS_BLANK
    MOV R0, R7
    BL GET_SEG_DIGIT
    MOV R7, R0
    B DISPLAY_RESULT_7SEG_HUNDREDS_DONE

DISPLAY_RESULT_7SEG_HUNDREDS_BLANK:
    MOV R7, #0

DISPLAY_RESULT_7SEG_HUNDREDS_DONE:
    @ monta HEX3..HEX0 = dezenas, unidades, _, decimal
    MOV R0, R6
    ORR R0, R0, #0x00000800
    ORR R0, R0, R5, LSL #16
    ORR R0, R0, R8, LSL #24

    LDR R1, =0xFF200020
    STR R0, [R1]

    @ monta HEX5..HEX4 = sinal, centenas
    MOV R0, R7
    ORR R0, R0, R9, LSL #8

    LDR R1, =0xFF200030
    STR R0, [R1]

    POP {R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, LR}
    BX LR
