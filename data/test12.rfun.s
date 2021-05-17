
  .globl main
main:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14

  movq $16384, %rdi
  movq $16, %rsi
  callq initialize
  movq rootstack_begin(%rip), %r15

  jmp main_start
label_12:
  movq $10, %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_13:
  movq $9, %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_14:
  cmpq $1, %rdx
  je label_12
  jmp label_13
label_15:
  jmp label_14
label_16:
  jmp label_15
label_17:
  movq $5, %rax
  cmpq $3, %rax
  setl %al
  movzbq %al, %rdx
  jmp label_16
label_18:
  movq $1, %rdx
  jmp label_16
label_19:
  movq $50, %rax
  cmpq $23, %rax
  setl %al
  movzbq %al, %rdx
  cmpq $1, %rdx
  je label_17
  jmp label_18
label_20:
  movq $0, %rdx
  jmp label_15
label_21:
  movq $6, %rdx
  addq $7, %rdx
  movq $3, %rax
  cmpq %rdx, %rax
  jl label_19
  jmp label_20
label_22:
  movq $0, %rdx
  jmp label_14
main_start:
  movq $5, %rax
  cmpq $6, %rax
  je label_21
  jmp label_22
main_conclusion:

  movq %rax, %rdi
  callq print_int
  movq $0, %rax

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq
