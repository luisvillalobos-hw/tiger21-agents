"use client"

import React from "react"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { Send, Building2, MapPin, DollarSign } from "lucide-react"
import { queryAnalysis, formatChatMessage, type ChatMessage, type StreamUpdate } from "@/lib/crewAIAuth"

interface Message {
  id: string
  content: string
  isUser: boolean
  timestamp: Date
  thinking?: string[]
  showThinking?: boolean
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      content:
        "Hello! I'm your AI deal sourcing agent. I can help you find investment opportunities in real estate and business deals. What type of opportunities are you looking for?",
      isUser: false,
      timestamp: new Date(),
    },
  ])
  const [inputValue, setInputValue] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [currentThinking, setCurrentThinking] = useState<string[]>([])
  const [streamingMessageId, setStreamingMessageId] = useState<string | null>(null)

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue,
      isUser: true,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    const currentInputValue = inputValue
    setInputValue("")
    setIsLoading(true)
    setCurrentThinking([])

    // Create streaming message
    const streamingMessageId = (Date.now() + 1).toString()
    setStreamingMessageId(streamingMessageId)

    const initialAiMessage: Message = {
      id: streamingMessageId,
      content: "Starting analysis...",
      isUser: false,
      timestamp: new Date(),
      thinking: [],
      showThinking: false,
    }

    setMessages((prev) => [...prev, initialAiMessage])

    try {
      // Call analysis system with streaming
      const response = await queryAnalysis(currentInputValue, (update: StreamUpdate) => {
        if (update.type === 'thinking') {
          setCurrentThinking((prev) => [...prev, update.data])

          // Update the streaming message with thinking
          setMessages((prev) =>
            prev.map(msg =>
              msg.id === streamingMessageId
                ? { ...msg, thinking: [...(msg.thinking || []), update.data] }
                : msg
            )
          )
        } else if (update.type === 'status') {
          // Update the main content with status
          setMessages((prev) =>
            prev.map(msg =>
              msg.id === streamingMessageId
                ? { ...msg, content: update.data }
                : msg
            )
          )
        }
      })

      if (response.error) {
        throw new Error(response.error)
      }

      // Update with final result and keep thinking visible
      setMessages((prev) =>
        prev.map(msg =>
          msg.id === streamingMessageId
            ? {
                ...msg,
                content: response.analysis || "Analysis completed",
                thinking: [...(msg.thinking || [])], // Keep all thinking steps
                showThinking: msg.thinking && msg.thinking.length > 0 // Auto-expand if there are thinking steps
              }
            : msg
        )
      )

    } catch (error) {
      console.error('Error calling analysis system:', error)

      let errorMessage = "I'm having trouble connecting to the analysis system. "

      if (error instanceof Error) {
        if (error.message.includes('analysis')) {
          errorMessage += "🚀 The system might be processing other requests. Please try again in a moment!"
        } else if (error.message.includes('timeout')) {
          errorMessage += "⏱️ The analysis is taking longer than expected. We're conducting thorough research."
        } else {
          errorMessage += "Please check the connection and try again later."
        }
      }

      setMessages((prev) =>
        prev.map(msg =>
          msg.id === streamingMessageId
            ? { ...msg, content: `⚠️ ${errorMessage}` }
            : msg
        )
      )
    } finally {
      setIsLoading(false)
      setStreamingMessageId(null)
      setCurrentThinking([])
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  return (
    <div className="h-screen flex flex-col bg-white">
      {/* Header - Clean and minimal like ChatGPT */}
      <div className="flex-shrink-0 border-b border-gray-200 bg-white">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-center gap-3">
            <div className="p-2 bg-blue-500 rounded-lg">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <h1 className="text-xl font-semibold text-gray-800">
              HW Deal<span className="text-blue-600">Sourcing</span>
            </h1>
          </div>
        </div>
      </div>

      {/* Chat Container - Full canvas like ChatGPT */}
      <div className="flex-1 overflow-hidden">
        <div className="h-full max-w-6xl mx-auto flex flex-col">
          {/* Messages Area - Scrollable */}
          <div className="flex-1 overflow-y-auto px-4 py-6">
            <div className="space-y-6">
              {messages.map((message) => (
                <div key={message.id} className={`flex ${message.isUser ? "justify-end" : "justify-start"}`}>
                  <div className={`flex gap-3 max-w-5xl w-full ${message.isUser ? "flex-row-reverse" : ""}`}>
                    {/* Avatar */}
                    <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                      message.isUser ? "bg-blue-500" : "bg-gray-200"
                    }`}>
                      {message.isUser ? (
                        <span className="text-white text-xs font-medium">You</span>
                      ) : (
                        <Building2 className="h-4 w-4 text-gray-600" />
                      )}
                    </div>

                    {/* Message Content */}
                    <div className="flex-1 min-w-0">
                      {/* Thinking Process */}
                      {!message.isUser && message.thinking && message.thinking.length > 0 && (
                        <div className="mb-3">
                          <button
                            onClick={() => {
                              setMessages(prev =>
                                prev.map(msg =>
                                  msg.id === message.id
                                    ? { ...msg, showThinking: !msg.showThinking }
                                    : msg
                                )
                              )
                            }}
                            className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-800 transition-colors"
                          >
                            <span className={`transform transition-transform ${message.showThinking ? 'rotate-90' : ''}`}>
                              ▶
                            </span>
                            <span>View thinking process ({message.thinking.length} steps)</span>
                          </button>

                          {message.showThinking && (
                            <div className="mt-2 p-3 bg-gray-50 rounded-lg border-l-4 border-blue-200">
                              <div className="space-y-2">
                                {message.thinking.map((step, index) => (
                                  <div key={index} className="text-sm text-gray-700 flex items-start gap-2">
                                    <span className="text-blue-500 font-mono text-xs mt-0.5">{index + 1}.</span>
                                    <span className="break-words">{step}</span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}
                        </div>
                      )}

                      {/* Main Content */}
                      <div className="prose prose-gray max-w-none">
                        <div
                          className="text-gray-800 leading-relaxed break-words"
                          dangerouslySetInnerHTML={{ __html: message.content }}
                        />
                      </div>
                      <div className="text-xs text-gray-500 mt-2">
                        {message.timestamp.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="flex gap-3 max-w-3xl">
                    <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">
                      <Building2 className="h-4 w-4 text-gray-600" />
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 text-gray-600">
                        <div className="flex gap-1">
                          <div className="w-2 h-2 bg-current rounded-full animate-bounce" />
                          <div
                            className="w-2 h-2 bg-current rounded-full animate-bounce"
                            style={{ animationDelay: "0.1s" }}
                          />
                          <div
                            className="w-2 h-2 bg-current rounded-full animate-bounce"
                            style={{ animationDelay: "0.2s" }}
                          />
                        </div>
                        <span className="text-sm">Analyzing opportunities...</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Input Area - Fixed at bottom like ChatGPT */}
          <div className="flex-shrink-0 border-t border-gray-200 bg-white">
            <div className="px-4 py-4 max-w-6xl mx-auto">
              <div className="flex gap-3 items-end">
                <div className="flex-1">
                  <Input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyPress={handleKeyPress}
                    placeholder="Ask me about real estate, M&A deals, investment opportunities..."
                    className="min-h-[44px] resize-none border-gray-300 focus:border-blue-500 focus:ring-blue-500 rounded-xl px-4"
                    disabled={isLoading}
                  />
                </div>
                <Button
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isLoading}
                  className="h-11 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-xl"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions - Fixed at bottom */}
      <div className="flex-shrink-0 bg-gray-50 border-t border-gray-200">
        <div className="max-w-6xl mx-auto px-4 py-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button
              variant="outline"
              className="h-auto p-4 bg-white border-gray-200 hover:bg-gray-50 rounded-xl transition-all duration-200"
              onClick={() => setInputValue("Find multifamily properties under $5M in Denver, Colorado")}
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-blue-50 rounded-lg">
                  <Building2 className="h-5 w-5 text-blue-600" />
                </div>
                <div className="text-left">
                  <p className="font-medium text-gray-900">Denver Multifamily</p>
                  <p className="text-sm text-gray-500">Under $5M Properties</p>
                </div>
              </div>
            </Button>

            <Button
              variant="outline"
              className="h-auto p-4 bg-white border-gray-200 hover:bg-gray-50 rounded-xl transition-all duration-200"
              onClick={() => setInputValue("Search for multifamily apartment buildings in Austin, Texas market")}
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-green-50 rounded-lg">
                  <Building2 className="h-5 w-5 text-green-600" />
                </div>
                <div className="text-left">
                  <p className="font-medium text-gray-900">Austin Multifamily</p>
                  <p className="text-sm text-gray-500">Texas Market</p>
                </div>
              </div>
            </Button>

            <Button
              variant="outline"
              className="h-auto p-4 bg-white border-gray-200 hover:bg-gray-50 rounded-xl transition-all duration-200"
              onClick={() => setInputValue("Find multifamily investment opportunities in Phoenix, Arizona with high cap rates")}
            >
              <div className="flex items-center gap-3">
                <div className="p-2 bg-purple-50 rounded-lg">
                  <MapPin className="h-5 w-5 text-purple-600" />
                </div>
                <div className="text-left">
                  <p className="font-medium text-gray-900">Phoenix Multifamily</p>
                  <p className="text-sm text-gray-500">High Cap Rates</p>
                </div>
              </div>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}