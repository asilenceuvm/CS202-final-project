
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
label_73:
  movq free_ptr(%rip), %rdx
  addq $32, free_ptr(%rip)
  movq %rdx, %r11
  movq $7, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 16(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r13, 24(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %r11
  movq 24(%r11), %rcx
  movq %rdx, %r11
  movq $38, 24(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq 24(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_74:
  movq $0, %rdx
  jmp label_73
label_75:
  movq %r15, %rdi
  movq $32, %rsi
  callq collect
  jmp label_73
main_start:
  movq $1, %rbx
  movq $2, %r12
  movq $3, %r13
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $32, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_74
  jmp label_75
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
