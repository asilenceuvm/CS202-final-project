
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
label_30:
  movq $20, %rax
  cmpq $7, %rax
  setl %al
  movzbq %al, %rdx
  movq %rdx, %rdx
  xorq $1, %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_31:
  movq $0, %rdx
  movq %rdx, %rax
  jmp main_conclusion
main_start:
  movq $6, %rax
  cmpq $5, %rax
  jl label_30
  jmp label_31
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
