
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
label_55:
  movq free_ptr(%rip), %rdx
  addq $24, free_ptr(%rip)
  movq %rdx, %r11
  movq $5, 0(%r11)
  movq %rdx, %r11
  movq %rbx, 8(%r11)
  movq $0, %rcx
  movq %rdx, %r11
  movq %r12, 16(%r11)
  movq $0, %rcx
  movq %rdx, %rdx
  movq %rdx, %r11
  movq 16(%r11), %rdx
  movq %rdx, %rax
  jmp main_conclusion
label_56:
  movq $0, %rdx
  jmp label_55
label_57:
  movq %r15, %rdi
  movq $24, %rsi
  callq collect
  jmp label_55
main_start:
  movq $1, %rbx
  movq $2, %r12
  movq free_ptr(%rip), %rdx
  movq %rdx, %rdx
  addq $24, %rdx
  movq fromspace_end(%rip), %rcx
  cmpq %rcx, %rdx
  jl label_56
  jmp label_57
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
