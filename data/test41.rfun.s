
  .globl id
id:
  pushq %rbp
  movq %rsp, %rbp
  subq $0, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp id_start
id_start:
  movq %rdi, %rdx
  movq %rdx, %rdx
  movq %rdx, %rax
  jmp id_conclusion
id_conclusion:

  addq $0, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

  .globl addup
addup:
  pushq %rbp
  movq %rsp, %rbp
  subq $80, %rsp
  pushq %rbx
  pushq %r12
  pushq %r13
  pushq %r14


  jmp addup_start
addup_start:
  movq $25, %rdx
  movq $26, %r9
  movq $26, %r13
  movq $26, %r10
  movq $26, -80(%rbp)
  movq $26, %rbx
  movq $26, -72(%rbp)
  movq $26, %r14
  movq $26, -88(%rbp)
  movq $26, -56(%rbp)
  movq $26, %r12
  movq $26, -48(%rbp)
  movq $26, -64(%rbp)
  movq $26, -24(%rbp)
  movq $26, -40(%rbp)
  movq $26, %rsi
  movq $26, -32(%rbp)
  movq $26, %rdi
  movq $26, %r8
  movq $26, %rcx
  movq $26, -16(%rbp)
  leaq id(%rip), %rdx
  movq %rcx, %rcx
  addq -16(%rbp), %rcx
  movq %r8, %r8
  addq %rcx, %r8
  movq %rdi, %rcx
  addq %r8, %rcx
  movq -32(%rbp), %rdi
  addq %rcx, %rdi
  movq %rsi, %rcx
  addq %rdi, %rcx
  movq -40(%rbp), %rsi
  addq %rcx, %rsi
  movq -24(%rbp), %rcx
  addq %rsi, %rcx
  movq -64(%rbp), %rsi
  addq %rcx, %rsi
  movq -48(%rbp), %rcx
  addq %rsi, %rcx
  movq %r12, %rsi
  addq %rcx, %rsi
  movq -56(%rbp), %rcx
  addq %rsi, %rcx
  movq -88(%rbp), %rsi
  addq %rcx, %rsi
  movq %r14, %rcx
  addq %rsi, %rcx
  movq -72(%rbp), %rsi
  addq %rcx, %rsi
  movq %rbx, %rcx
  addq %rsi, %rcx
  movq -80(%rbp), %rsi
  addq %rcx, %rsi
  movq %r10, %rcx
  addq %rsi, %rcx
  movq %r13, %rsi
  addq %rcx, %rsi
  movq %r9, %rcx
  addq %rsi, %rcx
  movq %rcx, %rdi
  movq %rdx, %rax
  
  addq $80, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  jmp *%rax

addup_conclusion:

  addq $80, %rsp
  subq $0, %r15
  popq %r14
  popq %r13
  popq %r12
  popq %rbx
  popq %rbp
  retq

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
main_start:
  leaq addup(%rip), %rdx
  movq %rdx, %rax
  callq *%rax
  jmp main_conclusion
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
