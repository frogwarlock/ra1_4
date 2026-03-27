.data
AUX_ZERO: .double 0.0
AUX_ONE: .double 1.0
TMP_Q: .double 0.0
TMP_A: .double 0.0
TMP_B: .double 0.0
TMP_BASE: .double 0.0
TMP_RES: .double 0.0
TMP_EXP_I: .double 0.0
CONST_0: .double 2.60
CONST_1: .double 1.4
CONST_2: .double 10.0
CONST_3: .double 3
CONST_4: .double 2
CONST_5: .double 4
CONST_6: .double 9.8
CONST_7: .double 3.2
CONST_8: .double 8
CONST_9: .double 9
CONST_10: .double 1
CONST_11: .double 2.0
CONST_12: .double 5
CONST_13: .double 0
CONST_14: .double 12.0
MEM_X: .double 0.0
RES_0: .double 0.0
RES_1: .double 0.0
RES_2: .double 0.0
RES_3: .double 0.0
RES_4: .double 0.0
RES_5: .double 0.0
RES_6: .double 0.0
RES_7: .double 0.0
RES_8: .double 0.0
RES_9: .double 0.0
TEMP_0: .double 0.0
TEMP_1: .double 0.0
TEMP_2: .double 0.0
TEMP_3: .double 0.0
TEMP_4: .double 0.0
TEMP_5: .double 0.0
TEMP_6: .double 0.0
TEMP_7: .double 0.0
TEMP_8: .double 0.0
TEMP_9: .double 0.0
TEMP_10: .double 0.0
TEMP_11: .double 0.0
TEMP_12: .double 0.0
TEMP_13: .double 0.0
TEMP_14: .double 0.0
TEMP_15: .double 0.0
TEMP_16: .double 0.0
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
    LDR R0, =CONST_6
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_7
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
    LDR R0, =CONST_8
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_3
    VLDR.F64 D1, [R1]
    BL INTEGER_DIV_64
    LDR R2, =TEMP_7
    VSTR.F64 D0, [R2]
    @ operacao VADD.F64
    LDR R0, =TEMP_7
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_4
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
    LDR R0, =CONST_9
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_5
    VLDR.F64 D1, [R1]
    BL MODULO_64
    LDR R2, =TEMP_9
    VSTR.F64 D0, [R2]
    @ operacao VADD.F64
    LDR R0, =TEMP_9
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_10
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
    LDR R0, =CONST_11
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_3
    VLDR.F64 D1, [R1]
    BL EXPONENTIATION_64
    LDR R2, =TEMP_11
    VSTR.F64 D0, [R2]
    @ operacao VSUB.F64
    LDR R0, =TEMP_11
    VLDR.F64 D0, [R0]
    LDR R1, =CONST_10
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
    LDR R1, =CONST_12
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
    LDR R1, =CONST_14
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
